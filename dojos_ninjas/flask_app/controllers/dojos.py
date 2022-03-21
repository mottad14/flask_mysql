from flask_app import app
from flask import render_template,redirect,request
# ...server.py

from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route('/dojos')
def index():
    return render_template("dojos.html", all_dojos = Dojo.get_all()) 

@app.route('/createDojo',methods=['POST'])
def create():
    data = {
        "name":request.form['name']
    }
    Dojo.save(data)
    return redirect('/dojos')



#Render the ninja create page
@app.route('/ninjas')
def ninjaForm():
    return render_template("Ninjas.html",all_dojos=Dojo.get_all())

#Process the ninja create page

@app.route('/createNinja', methods = ['POST'])
def createNinja():
    # (first_name,last_name,age,Dojo_id,created_at,updated_at)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age":request.form['age'],
        "Dojo_id":request.form.get('Dojo_id')
    }
    Ninja.save(data)
    return redirect("/dojos/" + data["Dojo_id"])




@app.route('/dojos/<int:dojo_id>')
def detail_page(dojo_id):
    data = {
        'id': dojo_id,
    }
    return render_template("Dojo_show.html", all_ninjas=Dojo.get_dojo_with_ninjas(data))

@app.route('/edit_page/<int:burger_id>')
def edit_page(burger_id):
    data = {
        'id': burger_id,
    }
    return render_template("edit_page.html", burger = Burger.get_one(data))

@app.route('/update/<int:burger_id>', methods=['POST'])
def update(burger_id):
    data = {
        'id': burger_id,
        "name":request.form['name'],
        "bun": request.form['bun'],
        "meat": request.form['meat'],
        "calories": request.form['calories']
    }
    Burger.update(data)
    return redirect(f"/show/{burger_id}")

@app.route('/delete/<int:burger_id>')
def delete(burger_id):
    data = {
        'id': burger_id,
    }
    Burger.destroy(data)
    return redirect('/burgers')