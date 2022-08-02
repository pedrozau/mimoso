from flask import Flask 
from  vite.extension import configuration




def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app
    
def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1python1@localhost/mimoso"
