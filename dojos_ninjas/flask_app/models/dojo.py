from flask_app.models import ninja
from flask_app.config.mysqlconnection import connectToMySQL

class Dojo:
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # This is the list where we can an add in all the ninjas that are associated with the Dojo.
        self.ninjas = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO Dojos ( name , created_at , updated_at ) VALUES (%(name)s,NOW(),NOW());"
        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM Dojos;"
        dojos_from_db =  connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        dojos =[]
        for d in dojos_from_db:
            dojos.append(cls(d))
        return dojos
    
    ...
    @classmethod
    def get_dojo_with_ninjas( cls , data ):
        query = "SELECT * FROM Dojos LEFT JOIN Ninjas ON Ninjas.Dojo_id = Dojos.id WHERE Dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db( query , data )
        # results will be a list of topping objects with the ninja attached to each row. 
        Dojo = cls(results[0])
        for row_from_db in results:
            # Now we parse the burger data to make instances of burgers and add them into our list.
            Ninja_data = {
                "id" : row_from_db["Ninjas.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "age" : row_from_db["age"],
                "created_at" : row_from_db["Ninjas.created_at"],
                "updated_at" : row_from_db["Ninjas.updated_at"]
            }
            Dojo.ninjas.append( ninja.Ninja( Ninja_data ) )
        return Dojo.ninjas
