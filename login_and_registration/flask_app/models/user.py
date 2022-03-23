from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL('login_register_schema').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_from_db =  connectToMySQL('login_register_schema').query_db(query)
        users =[]
        for one_user in users_from_db:
            users.append(cls(one_user))
        return users
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        user_from_db = connectToMySQL('login_register_schema').query_db(query,data)

        return cls(user_from_db[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_register_schema").query_db(query,data)
        #If the result find no matching user
        if len(result) < 1:
            return False
        return cls(result[0])



#********** VALIDATION CODE FOR USER REGISTRATION BELOW **********
    # Other User methods up yonder.
    # Static methods don't have self or cls passed into the parameters.
    # We do need to take in a parameter to represent our user
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
            #RESERVED FOR EMAIL AND PASSWORD COMMANDS
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be 8 characters or more")
            is_valid = False
        if (user['confirm_password']) != (user['password']):
            flash("Passwords must match")
            is_valid = False
        return is_valid





    # @classmethod
    # def update(cls,data):
    #     query = "UPDATE burgers SET name=%(name)s, bun=%(bun)s, meat=%(meat)s, calories=%(calories)s,updated_at = NOW() WHERE id = %(id)s;"
    #     return connectToMySQL('login_reg').query_db(query,data)

    # @classmethod
    # def destroy(cls,data):
    #     query = "DELETE FROM burgers WHERE id = %(id)s;"
    #     return connectToMySQL('login_reg').query_db(query,data)
