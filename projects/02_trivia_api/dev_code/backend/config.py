import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

database_setup = {
    'database_name': 'trivia',
    'database_name_test': 'trivia_test',
    'user_name': 'postgres',  
    'password': None,  
    'port': 'localhost:5432' 
}
