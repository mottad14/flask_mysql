from flask_app import app
from flask_app.models.user import User
from flask import render_template, request, redirect, session, flash
#Get bcrypt for login and reg - userController
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




#Index route for login and registration
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def create_user():
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":request.form['password'],
        "confirm_password":request.form['confirm_password'],
    }
    # We call the static method on User model to validate
    if not User.validate_user(request.form):
        # if errors, redirect to the route where the user form is rendered.
        return redirect('/')

    
    # else no errors:
    #create a password hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print("THIS IS THE PW HASH", pw_hash)

    #Going to put the password-hash into data dictionary
    data['password'] = pw_hash
    print ("THIS IS THE NEW DATA DICTIONARY that should include the hashed password", data)

#User.save now takes all our validated form data (including hashed+salted pw) 
# and saves it - the query then sends back the new id
# here I store the ID in session so as to show that the user is logged in     
    session['id'] = User.save(data) 
   
    return redirect("/registerSuccess")


@app.route('/registerSuccess')
def confirmRegister():    
    # created data dictionary with id from session to pass to query method
    data ={
        "id":session['id']
    }
    user = User.get_one(data)
    # calls get_one method, assign object returned to variable
    # pass user object to render template function
    return render_template('success.html', user = user)

@app.route('/logIn', methods=['POST'])
def loginConfirm():
    data = {
        "email": request.form['email'],
    }
    #This calls upon the function in users model, 
    user_in_db = User.get_by_email(data)
    
    #Check to see if email is in the database
    if not user_in_db:
        flash("The email or password you provided is not correct")
        return redirect('/')

    #Check to see if hashed+salted pw in the database 
    # matches the pw being passed in
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ("The email or password you provided is not correct")
        return redirect('/')

    session['id'] = user_in_db.id


    return redirect("/logInSuccess")
    

@app.route('/logInSuccess')
def loggedIn():
    data = {
        'id':session['id']
    }
    user = User.get_one(data)
    #Grab the name of the person
    return render_template('loggedIn.html', user = user)
