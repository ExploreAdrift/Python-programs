# allows our model to talk to db
import email
from urllib.parse import quote_plus
from flask_app.config.mysqlconnection import connectToMySQL
# allows us flash messages onto html page (EX email doesnt exist)
from flask import flash

# allows us to use global DATABASE variable
from flask_app import DATABASE

# allows REGEX to validate emails
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

# time to build class


class User:
    def __init__(self, data):
        # refer to tables in db to ensire you have required columns/attributes
        # all atributes must refer to the variable passed(data) and a key
        # use [] and quotes give key
        # ensure all attribute names match the column name in the db
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.pw_hash = data["pw_hash"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # put any methods here to required to access by indivual instances of this class
        # these are actions that  a single instance of this class performs (user.do_something)

        # write class methods here(all methods willpass through cls at a minimum)

        # classmethod to create new user, requires  us to pass user information in using data
    @classmethod
    def new_user(cls, data):
        # query is the exact copy you would enter into mysql, inside of the quotes
        # use the %()s to mogrify the data and prevent sql injection into our DB
        query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at)"
        query += "VALUES (%(first_name)s, %(last_name)s,%(email)s,%(pw_hash)s, NOW(), NOW());"
        # send the query to your mySQL database to save the new user in the users table
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # this will retrieve user_id
    @classmethod
    def get_one(cls, data):
        # we need to query the db to grab the instance of the user by  id
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # here we want to return only the first rowas a dictionary with the data selected from the selected id
        return cls(result[0])

        # this method will get user by email
        # if the email doesnt exist in the db it will return False
        # if the email exists it will return the row with the user info

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
       # static methods here (apply to instance of this class without effecting the class)
    # usually used for validation and to check data in the class witout changing the data.

    # singular version of class (table) (in this case it is "user")
    # this method checks that all fields have something entered
    # flashes a message if there is nothing entered into the field

    @staticmethod
    def validate_all_present(user):
        if not len(user["first_name"]) > 0:
            flash("You must enter a first name")
            return False

        if not len(user["last_name"]) > 0:
            flash("You must enter a last name")
            return False

        if not len(user["email"]) > 0:
            flash("You must enter a an email")
            return False

        if not len(user["pw"]) > 0:
            flash("You must enter a password")
            return False

        if not len(user["pw1"]) > 0:
            flash("You must confirm your password")
            return False
        return True

    # This method will validate name length and that both passowrds match
    @staticmethod
    def validate_user(user):
        if not len(user["first_name"]) > 2:
            flash("first name must be atleast 2 characters")
            return False
        if not len(user["last_name"]) > 2:
            flash("first name must be atleast 2 characters")
            return False
        if not user["pw"] == user["pw1"]:
            flash("Passwords must match!")
            return False
        return True

    # THIS STATIC METHOD WILL VALIDATE EMAIL FORMAT IS CORRECT
    @staticmethod
    def validate_email(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("invalid email address")
            is_valid = False
        return is_valid

    # THIS METHOD WILL SEE IF THE EMAIL ACTUALLY EXISTS IN THE DB REFER TO (GET_BY-EMAIL DEF)
    # IF EMAIL EXISTS, IT WILL NOT ALLOW THEM TO CREATE AN ACCOUNT
    # AFTER THAT IS COMPLETED CONTINUE TO STATIC METHOD (DOES THE EMAIL EXIST?)
    @staticmethod
    def email_exist(user):
        if User.get_by_email(user):
            flash("This email is already in use")
            return False
        return True
