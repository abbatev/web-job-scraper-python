from flask_app.config.connect_sql import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime

class Listing:
    db="listings"
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.date = data['date']
        self.description = data['description']
        self.details = data['details']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None
    

    #create
    @classmethod
    def create_listing(cls, data):
        query = """
        INSERT INTO listings (url, date, description, details, notes, user_id)
        VALUES (%(url)s, %(date)s, %(description)s, %(details)s, %(notes)s, %(user_id)s)
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    #read

    #get all
    @classmethod
    def get_all_listings(cls):
        query="""
        SELECT * FROM listings
        JOIN users ON listings.user_id=users.id 
        """

        results=connectToMySQL(cls.db).query_db(query)

        all_listings=[]

        for row in results:
            one_listing=cls(row)

            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'], 
            }
            one_listing.owner=user.User(user_data)
            all_listings.append(one_listing)
        return all_listings

#get one
    @classmethod
    def get_one_listing(cls, data):
        query="""
        SELECT * FROM listings
        JOIN users ON listings.user_id=users.id
        WHERE listings.id=%(id)s;
        """
        results=connectToMySQL(cls.db).query_db(query,data)
        one_listing=cls(results[0])
        user_data={ 
        'id' :results[0]['users.id'],
        'first_name' :results[0]['first_name'],
        'last_name' :results[0]['last_name'],
        'email' :results[0]['email'],
        'password' :results[0]['password'],
        'created_at' :results[0]['created_at'],
        'updated_at' :results[0]['updated_at'], 
        }
        one_listing.owner=user.User(user_data)
        return one_listing

    #update
    @classmethod
    def update_listing(cls, data):
        query="""
        UPDATE listings
        SET url=%(url)s, date=%(date)s, description=%(description)s, details=%(details)s, notes=%(notes)s
        WHERE id=%(id)s; 
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
    #delete
    @classmethod
    def delete_listing(cls, data):
        query="""
        DELETE FROM listings
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    #validate
    @staticmethod
    def validate_listing(data):
        is_valid=True

        if len(data['url']) ==0:
            is_valid=False
            flash('Please enter a url', 'listing')
        elif len(data['url']) < 3:
            is_valid=False
            flash('Please enter at least 3 characters', 'listing')

        if len(data['date']) ==0:
            is_valid=False
            flash('Please enter a date', 'listing')
       
        if len(data['description']) ==0:
            is_valid=False
            flash('Please enter a description', 'listing')
        elif len(data['description']) >255:
            is_valid=False
            flash('Please use 255 characters or less', 'listing')

        if len(data['details']) ==0:
            is_valid=False
            flash('Please enter details', 'listing')
        elif len(data['details']) >255:
            is_valid=False
            flash('Please use 255 characters or less', 'listing')

        if len(data['details']) ==0:
            is_valid=False
            flash('Please enter details', 'listing')
        elif len(data['details']) >255:
            is_valid=False
            flash('Please use 255 characters or less', 'listing')
            
        return is_valid







