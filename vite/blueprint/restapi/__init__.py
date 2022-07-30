from flask import Blueprint 
from flask_restful import Api 
from .resources import Usuario
from .resources import Vendas 
from .resources import Login



bp = Blueprint("restapi",__name__,url_prefix="/api/v1")

api = Api(bp) 
api.add_resource(Login,"/auth/login")
api.add_resource(Usuario,"/users")
api.add_resource(Usuario,"/users/<int:id>")
api.add_resource(Vendas,"/vendas")



def init_app(app):
   
    app.register_blueprint(bp)