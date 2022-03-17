from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.ninja import Ninja

@app.route('/')
def index():
    return render_template("home.html", all_ninjas = Ninja.get_all())


@app.route('/createNinja' , methods=['POST'])
def create_ninja():
    Ninja.create(request.form)
    return redirect("/")