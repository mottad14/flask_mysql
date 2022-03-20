from flask import render_template,redirect,request

from flask_app import app

from flask_app.models.user import User

#Main Page on which User is Created 
@app.route('/')
def index():
    return render_template("create.html")

#Processes the input from the main page
@app.route('/create',methods=['POST'])
def create():
    data = {
        "first_name":request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
    }
    User.save(data)
    return redirect('/users')

#Shows table of users that are in the Database
@app.route('/users')
def burgers():
    return render_template("read.html",all_users=User.get_all())

#Below is burger - app project related work that wasn't integrated here
# @app.route('/show/<int:burger_id>')
# def detail_page(burger_id):
#     data = {
#         'id': burger_id
#     }
#     return render_template("details_page.html",burger=Burger.get_one(data))

# @app.route('/edit_page/<int:burger_id>')
# def edit_page(burger_id):
#     data = {
#         'id': burger_id
#     }
#     return render_template("edit_page.html", burger = Burger.get_one(data))

# @app.route('/update/<int:burger_id>', methods=['POST'])
# def update(burger_id):
#     data = {
#         'id': burger_id,
#         "name":request.form['name'],
#         "bun": request.form['bun'],
#         "meat": request.form['meat'],
#         "calories": request.form['calories']
#     }
#     Burger.update(data)
#     return redirect(f"/show/{burger_id}")

# @app.route('/delete/<int:burger_id>')
# def delete(burger_id):
#     data = {
#         'id': burger_id,
#     }
#     Burger.destroy(data)
#     return redirect('/burgers')