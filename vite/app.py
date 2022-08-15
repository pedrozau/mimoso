from flask import Flask 
from  vite.extension import configuration 
from  vite.extension import command





def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app
    
def create_app(**config):
    
    app = minimal_app(**config)
    configuration.load_extensions(app)
    command.create_db()
    return app


