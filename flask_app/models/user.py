from flask_app.config.connect_sql import connectToMySQL
from flask import flash
from flask_app import app, bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db="listings"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #create
    @classmethod
    def create_user(cls,data):
        query="""
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
            """
        return connectToMySQL(cls.db).query_db(query,data)


    #read
    
    @classmethod
    def get_user_by_id(cls, data):
        query="""
            SELECT * FROM users 
            WHERE id= %(user_id)s;
            """
        results=connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query= """
                SELECT * FROM users
                WHERE email=%(email)s;
            """
        results=connectToMySQL(cls.db).query_db(query,data)        
        if not results:
            return False
        
        return cls(results[0])
#validation
    @staticmethod
    def validate_registration(data): 
        is_valid=True
        one_user = User.get_user_by_email(data)
        if one_user:
            is_valid=False
            flash('This account already exists.', 'reg') 

        #fname 
        if len(data['first_name']) ==0: 
            is_valid=False
            flash('Please enter a first name.', 'reg')
        elif len(data['first_name']) < 2: 
            is_valid=False
            flash('Please enter a first name with at least 2 characters.', 'reg') 
                
        #lname
        if len(data['last_name']) ==0:
            is_valid=False
            flash('Please enter a last name.', 'reg')
        elif len(data['last_name']) < 2:
            is_valid=False
            flash('Please enter a  last name with at least 2 characters.', 'reg')        
        
        #email
        if len(data['email']) ==0:
            is_valid=False
            flash('Please enter an email.', 'reg')
        elif len(data['email']) < 8:
            is_valid=False
            flash('Please enter an email with at least 8 characters.', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid=False  
            flash('Invalid email format', 'reg')
        
        #pwd
        if len(data['password']) ==0:
            is_valid=False
            flash('Please enter a password.', 'reg')
        elif len(data['password']) < 3:
            is_valid=False
            flash('Please enter a password with at least 3 characters.', 'reg')
        
        #check pwd
        if len(data['password']) ==0:
            is_valid=False
            flash('Please enter a password confirmation.', 'reg')
        if data['password']!= data['conf_password']:
            is_valid=False
            flash("Passwords don't match.", 'reg')
        return is_valid
        
    @staticmethod
    def validate_login(data):
        one_user = User.get_user_by_email(data)
        if not one_user:
            flash("Nice try, pal. Create an account", 'login')
            return False
        if not bcrypt.check_password_hash(one_user.password, data['password']):
            flash("There's no accunt for that email.", 'login')
            return False
        
        
        return one_user  