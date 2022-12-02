from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = 'logInDB'
    def __init__(self, data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def addUser(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s ); '
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def getAllUsers(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(row)
        return users


    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s; '
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def getUserById(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(user_id)s; '
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]
    
    @staticmethod
    def validate_user(user):
        is_valid = True  #we assume this is true
        if len(user['first_name']) < 1:
            flash("First name is required to register", 'first_name')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name is required to register", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 1: 
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        if user['password']!=user['confirmPassword']:
            flash("Passwords are not matching", 'passwordConfirm')
            is_valid = False
        return is_valid