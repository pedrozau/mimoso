from flask import Flask 
from  vite.extension import configuration 
from  vite.extension import command 




def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app
    
def create_app(**config):
    command.create_db()
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app


#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1python1@localhost/mimoso"
