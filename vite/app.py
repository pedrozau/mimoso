from flask import Flask 
from  vite.extension import configuration 





def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app
    
def create_app(**config):
    
    app = minimal_app(**config)
    configuration.load_extensions(app)
    if __name__ == "__main__":
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    return app


