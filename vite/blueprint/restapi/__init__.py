from flask import Blueprint
from flask_restful import Api

from .resources import (Caixas, Caldas, Categorias, FecharCaixas, Golusemase,
                        Items, Login, Pedidos, Produtos, Sabores,
                        SearchPedidoVenda, SearchProduto, SearchVenda, Usuario,
                        Vendas)

bp = Blueprint('restapi', __name__, url_prefix='/api/v1')


api = Api(bp)

"""
Adicionando routas na minha blueprint.
"""
api.add_resource(Login, '/auth/login')
api.add_resource(Usuario, '/users', '/user/<int:usuario_id>')
api.add_resource(Vendas, '/vendas', '/venda/<int:venda_id>')
api.add_resource(SearchVenda, '/venda/search')
api.add_resource(FecharCaixas, '/fecharcaixa', '/fecharcaixa/<int:fechar_id>')
api.add_resource(Pedidos, '/pedidos', '/pedido/<int:pedido_id>')
api.add_resource(SearchPedidoVenda, '/pedido/search')
api.add_resource(Items, '/itens', '/itens/<int:id>')
api.add_resource(Produtos, '/produtos', '/produto/<int:produto_id>')
api.add_resource(SearchProduto, '/produto/seach')
api.add_resource(Categorias, '/categorias', '/categoria/<int:categoria_id>')
api.add_resource(Golusemase, '/golusemas', '/golusema/<int:golusema_id>')
api.add_resource(Sabores, '/sabores', '/sabor/<int:sabor_id>')
api.add_resource(Caldas, '/caldas', '/calda/<int:calda_id>')
api.add_resource(Caixas, '/caixas', '/caixa/<int:caixa_id>')


def init_app(app):

    app.register_blueprint(bp)
