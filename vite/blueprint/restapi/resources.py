from flask import jsonify, request
from flask_restful import Resource 
from vite.model import db
from vite.model import User
from vite.model import Venda
from vite.model import AbrirCaixa
from vite.model import FecharCaixa
from vite.model import PedidoVenda
from vite.model import ItensPedidoVenda
from vite.model import Produto
from vite.model import Categoria
from vite.model import Golusemas
from vite.model import Sabor
from vite.model import Calda




class Usuario(Resource):
    
    def get(self):
        
        user = User.query.all()
    
        return jsonify({"users": [users.to_dict()for users in user]})
    
    def post(self):
        message_error = ""
        data = request.get_json()
        
        try:
            user = User(nome=data['nome'],senha=data['senha'],foto=data['foto'],tipo_usuario=data['tipo_usuario'])
            db.session.add(user)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error":message_error
        })


class Vendas(Resource):
    
    def get(self):
        vendas = Venda.query.all()
        return jsonify({"vendas":[sell.to_dict()for sell in vendas]})
    
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            vendas = Venda(data=data['data'],pedido_id=data['pedido_id'],usuario_id=data['usuario_id'],valor=data['valor'])
            db.session.add(vendas)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
            
        return jsonify({
            "message_error":message_error
        })
        

class AbrirCaixas(Resource):
    
    def get(self):
        abrircaixa = AbrirCaixa.query.all()
        return jsonify({
            "abrir_caixa":[abrcaixa.to_dict() for abrcaixa in abrircaixa]
        })
        
    def post(self):
        message_error = ""
        data = request.get_json()
        try: 
            abrircaixa = AbrirCaixa(sumplemento=data['sumplemento'],despsas=data['despesas'],valorInicial=data['data_inicial'],dataAbertura=data['data_abertura'],usuario_id=data['usuario_id'],total=data['total'])
            db.session.add(abrircaixa)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        
        return jsonify({
            "message_error":message_error
        })
        

class FecharCaixa(Resource):
    
    def get(self):
        fecharcaixa = FecharCaixa.query.all()
        return jsonify({
            "fechar_caixa":[fechcaixa.to_dict() for fechcaixa in fecharcaixa]
        })
        
    def post(self):
        message_error = "" 
        data = request.get_json()
        try:
            fecharcaixa = FecharCaixa(despsas=data['despesas'],dataFechamento=data['data_fechamento'],usuario_id=data['usuario_id'],total=data['total'])
            db.session.add(fecharcaixa)
            db.session.commit()
        except Exception:
            message_error = "4743"
        
        return jsonify({
            "message_error":message_error
        })
        

class PedidoVendas(Resource):
    
    def get(self):
        pedidovenda = PedidoVenda.query.all()
        return jsonify({
            "pedido_venda":[pvenda.to_dict() for pvenda in pedidovenda]
        })
        
        
    def post(self):
        message_error = ""
        data = request.get_json() 
        try:
            pvenda = PedidoVenda(data=data['data'],quantidade=data['quantidade'],total=data['total'],itensPedidoVenda_id=data['itens_pedido_venda_id'])
            db.session.add(pvenda)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        
        return jsonify({
            "message_error":message_error
        })


class ItensPedidoVendas(Resource):
    def get(self):
        itpvenda = ItensPedidoVenda.query.all() 
        return jsonify({
            "itens_pedido_venda":[itens.to_dict() for itens in itpvenda]
        })
        
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            itens = ItensPedidoVenda(produto_id=data['produto_id'],quantidade=data['quantidade'])
            db.session.add(itens)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error":message_error
        })
        
        
class Produto(Resource):
    
    def get(self):
        produto = Produto.query.all()
        return jsonify({
            "produto":[prod.to_dict() for prod in produto]
        })
        
    def post(self):
        message_error = "" 
        data = request.get_json()
        try:
            prod = Produto(produto_nome=data['produto_nome'],preco=data['preco'],descricao_produto=data['descricao_produto'],unidade=data['unidade'],categoria_id=data['categoria_id'],sabor_id=data['sabor_id'],caldo_id=data['caldo_id'],golusemas_id=data['golusemas_id'])
            db.session.add(prod)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743" 
            
class Categoria(Resource):
    
    def get(self):
        categoria = Categoria.query.all()
        return jsonify({
            "categoria":[cat.to_dict() for cat  in categoria]
        })
    
    def post(self):
        message_error  = ""
        data = request.get_json()
        try:
            categoria = Categoria(nome=data['nome'])
            db.session.add(categorio)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"

class Golusemas(Resource):
    
    def get(self):
        golusemas = Golusemas.query.all()    
        return jsonify({
            "golusemas":[golese.to_dict()for golese  in golusemas]
        })    
    
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            golusemas = Golusemas(nome=data['nome'],unidade=data['unidade'])
            db.session.add(golusemas)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        
        return jsonify({
            "message_error":message_error       
        })


class Sabors(Resource):
    
    def get(self):
        sabor = Sabor.query.all()
        return jsonify({
            "sabor":[sab.to_dict()for sab in sabor]
        }) 
        
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            sabor = Sabor(nome=data['nome'],descricao_sabor=data['descricao_sabor'])
            db.sesssion.add(sabor)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
            
class Caldas(Resource):
    def get(self):
        calda = Calda.query.all()
        return jsonify({
            "calda":[cald.to_dict() for cald in calda]
        })
    
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            calda = Calda(nome=data['nome'],descricao_calda=data['descricao_calda'])
            db.session.add(calda)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        
        return jsonify({
            "message_error":message_error
        })