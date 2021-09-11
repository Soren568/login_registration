from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime, date


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = "login_registration_schema"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        self.gender = data['gender']
        self.account_type = data['account_type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password, dob, gender, account_type) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s, %(dob)s, %(gender)s, %(account_type)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        print("test", data)
        results = connectToMySQL(DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        
        # Name check - works
        if len(user['first_name']) < 1 or len(user['last_name']) < 1:
            flash("Please enter your name.", 'name')
            is_valid = False

        # email check - works
        e_query = "SELECT * FROM users WHERE email = %(email)s"
        e_results = connectToMySQL(DB).query_db(e_query,user)
        if len(e_results) > 0:
            flash("Email already registered.", "email")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email input.", "email")

        # Password confirmation check
        if len(user['password']) < 8:
            flash("Password not long enough.", "pw_length")
        if user['password'] != user['pw_confirm']:
            flash("Passwords did not match.", "pw_confirm")
            is_valid = False

        # DOB check - works, need to parse in order to find out if older than 18 years
        if user['dob'] == date.today().strftime("%Y-%m-%d"):
            # print(date.today().strftime("%Y-%m-%d"))
            # print(user['dob'])
            flash("Welcome to the world! Now please enter your actual birthday.", "dob")
            is_valid = False
        elif user['dob'] == '':
            flash("Please enter your birthday.", "dob")
            is_valid = False

# ! Doesnt work for gender check or account type check - bad keyerrors
        # # Gender Check: - doesnt work?
        # if user['gender'] not in ["male", "female", "other"]:
        #     flash("Please select one of the given options.", "gender")
        #     is_valid = False

        # # Account Type Check: 
        # if user['account_type'] not in ['fun', 'work', 'learning']:
        #     flash("Please select one of the given options.", "account_type")
        #     is_valid = False

        return is_valid

    @staticmethod
    def get_by_email(user):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DB).query_db(query,user)
        if len(results) < 1:
            return False
        return results[0]

    