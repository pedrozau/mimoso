from flask import Blueprint 
from flask_restful import Api 
from .resources import Usuario
from .resources import Vendas 
from .resources import Login
from .resources import AbrirCaixas 
from .resources import FecharCaixas
from .resources import PedidoVendas
from .resources import ItensPedidoVendas
from .resources import Produtos
from .resources import Categorias
from .resources import Golusemase
from .resources import Sabores 
from .resources import Caldas
from .resources import SearchPedidoVenda
from .resources import SearchProduto
from .resources import SearchVenda
from .resources import UploadFile 


bp = Blueprint("restapi",__name__,url_prefix="/api/v1")

api = Api(bp) 
api.add_resource(Login,"/auth/login")
api.add_resource(Usuario,"/users","/user/<int:id>")
api.add_resource(Vendas,"/vendas","/venda/<int:id>")
api.add_resource(SearchVenda,"/venda/search")
api.add_resource(AbrirCaixas,"/abrircaixa","/abrircaixa/<int:id>")
api.add_resource(FecharCaixas,"/fecharcaixa","/fecharcaixa/<int:id>")
api.add_resource(PedidoVendas,"/pedidovenda","/pedidovenda/<int:id>")
api.add_resource(SearchPedidoVenda,"/pedidovenda/search")
api.add_resource(ItensPedidoVendas,"/itenspedidovenda","/itenspedidovenda/<int:id>")
api.add_resource(Produtos,"/produtos","/produto/<int:id>")
api.add_resource(SearchProduto,"/produto/seach")
api.add_resource(Categorias,"/categorias","/categoria/<int:id>")
api.add_resource(Golusemase,"/golusemas","/golusema/<int:id>")
api.add_resource(Sabores,"/sabores","/sabor/<int:id>")
api.add_resource(Caldas,"/caldas","/calda/<int:id>")
api.add_resource(UploadFile,"/upload")


def init_app(app):
   
    app.register_blueprint(bp)