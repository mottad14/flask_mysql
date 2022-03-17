from flask_app.config.mysqlconnection import MySQLConnection

class Ninja:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.hometown = data['hometown']
        self.level = data['level']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas"
        res = MySQLConnection("ninjainfo").query_db(query)
        ninjas = []
        if len(res) == 0 :
            return "there is nothing in the list"

        for row in res:
            ninjas.append(cls(row))
        return ninjas
    @classmethod
    def create(cls,data):
        query = "INSERT INTO ninjas (name, homewn, level) VALUES (%(name)s,%(hometown)s,%(level)s,NOW())"
        return MySQLConnection("ninjainfo").query_db(query,data)

