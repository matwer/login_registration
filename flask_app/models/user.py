from flask import flash
from flask_bcrypt import Bcrypt
import re	# import the regex module
# create a regular expression object that we'll use later   

from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data ['password']
        self.crated_at = data['created_at']
        self.updated_at = data['updated_at']
        # palce holder for ice cream list. recipe list, etc


    # READ

    # Read Many
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL("login_reg_schema").query_db(query,data)

        user = cls(results[0])

        return user

    # Read One - gets one user and returns the user with a matching user id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL("login_reg_schema").query_db(query,data)

        user = cls(results[0])

        return user


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL("login_reg_schema").query_db(query,data)

        return cls(results[0]) if len(results) > 0 else None


    # creates a new user and inserts the user into the daatabase
    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) " \
            "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        
        user_id = connectToMySQL("login_reg_schema").query_db(query,data)

        return user_id


    # this is a static method - we just need to validate the data; we don't need 
    # references to the instance or the class
    @staticmethod
    def valid_registration(post_data): # post-data is the data we'll recieve from the form
        is_valid = True # we assume the data is valid so we set it to true at the star

        # flash is a message that exists for a single request-response cycle
        # for each validation, nottify the user and change the boolean to false
        if len(post_data['first_name']) < 3:
            flash("First name must be at least 3 characters") 
            is_valid = False 
    
        if len(post_data['last_name']) < 3:
            flash("Last name must be at least 3 characters") 
            is_valid = False 
    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(post_data['email']): 
            flash("Invalid email address")
            is_valid = False
        else:
            user_exists = User.get_by_email({"email": post_data['email']})
            if user_exists:
                flash("Email is already in use!")
                is_valid = False          
    
        if len(post_data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        
        if post_data['password'] != post_data['confirm_pw']:
            flash("Passwords must match")
            is_valid = False
    
        return is_valid

    @staticmethod
    def valid_login(post_data): # post-data is the data we'll recieve from the form
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash("Invalid Credentials")
            return False
        
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("Invalid Credentials")
            return False
        
        return True