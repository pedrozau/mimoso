from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from markupsafe import escape 
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
from .action import generate_token
from .action import token_required 

import werkzeug


""" 
variavel para directorio 

"""
UPLOAD_DIR = ""


"""
Routa para login requesito email e senha / method post 
"""


class Login(Resource):
    
    def remove_space(self,value):
        return value.replace(" ","")

    def post(self):
        data = request.get_json()
        message_error = ""
        if data['email'] == "" or data['senha'] == "":

            return jsonify({"message_error": "os campos estão vazios"})

        data_login = User.query.filter_by(email=escape(self.remove_space(data['email']))).first()

        if data_login is None:

            return jsonify({"message_error": "o usuario não existe"})

        if check_password_hash(data_login.senha, escape(self.remove_space(data['senha']))):
            try:
                data_login.token = generate_token(data_login.email)
                db.session.add(data_login)
                db.session.commit()
            except Exception as error:
                print(error)
                return jsonify({
                    "message_error": ""
                })

            return jsonify({"data": data_login.to_dict()})

        message_error = "a tua senha está incorreta tente novamente"

        return jsonify({"message_error": message_error})
    
    
"""
Routa para usuario fazer o logout  
"""


class Logout(Resource):
    def get(self):
        print('')


"""
Routa para usuarios   method get put post delete
"""


class Usuario(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @token_required
    def get(self):
        user = User.query.all()
        return jsonify({"users": [users.to_dict()for users in user]})
    
    def remove_space(self,value):
        return value.replace(" ","")

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        password_hash = generate_password_hash(
            self.remove_space(data['senha']), 15).decode('utf-8')
        foto = "user.png"
        token = generate_token(data['nome'])

        try:
            user = User(nome=data['nome'], email=self.remove_space(data['email']), senha=password_hash,
                        foto=foto, tipo_usuario=data['tipo_usuario'], token=token)
            db.session.add(user)
            db.session.commit()
            message_error = "o usuario foi cadastrado com sucesso"
        except Exception:
            message_error = f"já existe usuario cadastrado com esse nome {data['nome']} "

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self, id):

        user = User.query.filter_by(usuario_id=id).first()

        if user is None:
            jsonify({"message_error": "o usuario não foi encontrado"})
        try:
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message_error": "o usuario foi deletado com sucesso"})
        except Exception as error:

            return jsonify({
                "message_error": error
            })

    @token_required
    def put(self, id):
        user_update = User.query.filter_by(usuario_id=id).first()
        data = request.get_json()
        #file = request.files['foto']
        if 'nome' in data:
            user_update.nome = data['nome']
        elif 'email' in data:
            user_update.email = data['email']
        elif 'senha' in data:
            password_hash = generate_password_hash(
                data['senha'], 15).decode('utf-8')
            user_update.senha = password_hash
        elif 'foto' in data:
            """upload file  """
        
            user_update.foto = data['foto']
        elif 'tipo_usuario' in data:
            user_update.tipo_usuario = data['tipo_usuario']
        else:
            return jsonify({
                "message_error": "os campos estão vazio"
            })
        try:
            db.session.add(user_update)
            db.session.commit()
            return jsonify({
                "message_error": "actualizou com sucesso"
            })
        except Exception as error:
            print(error)
            return jsonify({
                "message_error": "problema ao atualizar os dados"
            })
            
class UploadFile(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def post(self):
         self.parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')
         args = self.parser.parse_args() 
         
         file = args.get("file")
         print(file.filename)
         
        
           

"""
Routa para vendas  method get put post delete
"""


class Vendas(Resource):

    @token_required
    def get(self):
        vendas = Venda.query.all()
        return jsonify({"vendas": [sell.to_dict()for sell in vendas]})

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            vendas = Venda(data=data['data'], pedidovenda_id=data['pedido_venda_id'],
                           usuario_id=data['usuario_id'], valor=data['valor'])
            db.session.add(vendas)
            db.session.commit()
            message_error = "cadastrou com sucesso"
        except Exception as error:
            print(error)
            message_error = "não cadastrou com sucesso"

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "campo vazio"})
        venda = Venda.query.filter_by(venda_id=id).first()
        if venda is None:
            jsonify({"message_error": "não foi econtrados as  vendas"})
        try:
            db.session.delete(venda)
            db.session.commit()
            return jsonify({"message_error": "venda foi deletado com sucesso"})
        except Exception as error:
            print(error)
            jsonify({"message_error": error})

    @token_required
    def put(self, id):
        venda_update = Venda.query.filter_by(venda_id=id).first()
        data = request.get_json()
        if 'data' in data:
            venda_update.data = data['data']
        elif 'pedidovenda_id' in data:
            venda_update.pedidovenda_id = data['pedidovenda_id']
        elif 'usuario_id' in data:
            venda_update.usuario_id = data['usuario_id']
        elif 'valor' in data:
            venda_update.valor = data['valor']
        else:
            return jsonify({
                "message": "campos vazios"
            })
        try:
            db.session.add(venda_update)
            db.session.commit()
        except Exception as error:
            print(error)
            return jsonify({
                "message": error
            })


"""
Routa para Abrircaixas method get put post delete
"""


class AbrirCaixas(Resource):

    @token_required
    def get(self):
        abrircaixa = AbrirCaixa.query.all()
        return jsonify({
            "abrir_caixa": [abrcaixa.to_dict() for abrcaixa in abrircaixa]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            abrircaixa = AbrirCaixa(sumplemento=data['sumplemento'], despsas=data['despesas'], valorInicial=data['data_inicial'],
                                    dataAbertura=data['data_abertura'], usuario_id=data['usuario_id'], total=data['total'])
            db.session.add(abrircaixa)
            db.session.commit()
            message_error = "cadastrou com sucesso"
        except Exception as error:
            print(error)
            message_error = error

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        abcaixa = AbrirCaixa.query.filter_by(venda_id=id).first()
        if abcaixa is None:
            jsonify({"message_error": "não foi encontrado"})
        try:
            db.session.delete(abcaixa)
            db.session.commit()
            return jsonify({"message_error": "cadastrou com sucesso"})
        except Exception as error:
            jsonify({"message_error": error})

    @token_required
    def put(self, id):
        acaixa_update = AbrirCaixa.query.filter_by(abrircaixa_id=id).first()
        data = request.get_json()

        if 'sumplemento' in data:
            acaixa_update.sumplemento = data['sumplemento']
        elif 'valor_inicial' in data:
            acaixa_update.valorInicial = data['valor_inicial']
        elif 'data_abertuta' in data:
            acaixa_update.dataAbertura = data['data_abertura']
        elif 'usuario_id' in data:
            acaixa_update.usuario_id = data['usuario_id']
        elif 'total' in data:
            acaixa_update.total = data['total']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(acaixa_update)
            db.session.commit()
            return jsonify({
                "message_error": "atualizou com sucesso"
            })
        except Exception as error:
            print(error)
            return jsonify({
                "message_error": error
            })


"""
Routa para Fecharcaixa  method get put post delete
"""


class FecharCaixas(Resource):

    @token_required
    def get(self):
        fecharcaixa = FecharCaixa.query.all()
        return jsonify({
            "fechar_caixa": [fechcaixa.to_dict() for fechcaixa in fecharcaixa]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            fecharcaixa = FecharCaixa(
                despsas=data['despesas'], dataFechamento=data['data_fechamento'], usuario_id=data['usuario_id'], total=data['total'])
            db.session.add(fecharcaixa)
            db.session.commit()
        except Exception:
            message_error = "4743"

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        fecharcaixa = FecharCaixa.query.filter_by(venda_id=id).first()
        if fecharcaixa is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(fecharcaixa)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        fcaixa_update = FecharCaixa.query.filter_by(fecharcaixa_id=id).first()
        data = request.get_json()

        if 'despesas' in data:
            fcaixa_update.despsas = data['despesas']
        elif 'data_fechamneto' in data:
            fcaixa_update.dataFechamento = data['data_fechamento']
        elif 'usuario_id' in data:
            fcaixa_update.usuario_id = data['usuario_id']
        elif 'total' in data:
            fcaixa_update.total = data['total']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(fcaixa_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para PedidoVenda  method get put post delete
"""


class PedidoVendas(Resource):

    @token_required
    def get(self):
        pedidovenda = PedidoVenda.query.all()
        return jsonify({
            "pedido_venda": [pvenda.to_dict() for pvenda in pedidovenda]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            pvenda = PedidoVenda(data=data['data'], quantidade=data['quantidade'],
                                 total=data['total'])
            db.session.add(pvenda)
            db.session.commit()
            message_error = "cadastrou com sucessso"
        except Exception as error:
            print(error)
            message_error = "não cadastro com sucesso"

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        pedidovenda = PedidoVenda.query.filter_by(venda_id=id).first()
        if pedidovenda is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(pedidovenda)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        pv_update = PedidoVenda.query.filter_by(pedidovenda_id=id).first()
        data = request.get_json()

        if 'data' in data:
            pv_update.data = data['data']
        elif 'quantidade' in data:
            pv_update.quantidade = data['quantidade']
        elif 'total' in data:
            pv_update.total = data['total']
        elif 'itensPedidoVenda_id' in data:
            pv_update.itensPedidoVenda_id = data['itensPedidoVenda_id']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(pv_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para ItensPedidoVendas   method get put post delete
"""


class ItensPedidoVendas(Resource):

    @token_required
    def get(self):
        itpvenda = ItensPedidoVenda.query.all()
        return jsonify({
            "itens_pedido_venda": [itens.to_dict() for itens in itpvenda]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            itens = ItensPedidoVenda(
                produto_id=data['produto_id'], quantidade=data['quantidade'])
            db.session.add(itens)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        itens = ItensPedidoVenda.query.filter_by(venda_id=id).first()
        if itens is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(itens)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        itpv_update = ItensPedidoVenda.query.filter_by(
            itenspedidovenda_id=id).first()
        data = request.get_json()

        if 'produto_id' in data:
            itpv_update.produto_id = data['produto_id']
        elif 'quantidade' in data:
            itpv_update.quantidade = data['quantidade']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(itpv_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para Produto   method get put post delete
"""


class Produtos(Resource):

    @token_required
    def get(self):
        produto = Produto.query.all()
        return jsonify({
            "produto": [prod.to_dict() for prod in produto]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            prod = Produto(produto_nome=data['produto_nome'], preco=data['preco'], descricao_produto=data['descricao_produto'], unidade=data['unidade'],
                           categoria_id=data['categoria_id'], sabor_id=data['sabor_id'], caldo_id=data['caldo_id'], golusemas_id=data['golusemas_id'])
            db.session.add(prod)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        prod = Produto.query.filter_by(venda_id=id).first()
        if prod is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(prod)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        produto_update = Produto.query.filter_by(produto_id=id).first()
        data = request.get_json()

        if 'produto_nome' in data:
            produto_update.produto_nome = data['produto_nome']
        elif 'preco' in data:
            produto_update.preco = data['preco']
        elif 'descricao_produto' in data:
            produto_update.descricao_produto = data['descricao_produto']
        elif 'unidade' in data:
            produto_update.unidade = data['unidade']
        elif 'categoria_id' in data:
            produto_update.categoria_id = data['categoria_Id']
        elif 'sabor_id' in data:
            produto_update.sabor_id = data['sabor_id']
        elif 'calda_id' in data:
            produto_update.calda_id = data['calda_id']
        elif 'golusemas_id' in data:
            produto_update.golusemas_id = data['golusemas_id']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(produto_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para Categoria   method get put post delete
"""


class Categorias(Resource):

    @token_required
    def get(self):
        categoria = Categoria.query.all()
        return jsonify({
            "categoria": [cat.to_dict() for cat in categoria]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            categoria = Categoria(nome=data['nome'])
            db.session.add(categoria)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        categoria = Categoria.query.filter_by(venda_id=id).first()
        if categoria is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(categoria)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        categoria_update = Categoria.query.filter_by(sabor_id=id).first()
        data = request.get_json()

        if 'nome' in data:
            categoria_update.nome = data['nome']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(categoria_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para Golusemase  method get put post delete
"""


class Golusemase(Resource):

    @token_required
    def get(self):
        golusemas = Golusemas.query.all()
        return jsonify({
            "golusemas": [golese.to_dict()for golese in golusemas]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            golusemas = Golusemas(nome=data['nome'], unidade=data['unidade'])
            db.session.add(golusemas)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        goluse = Golusemas.query.filter_by(venda_id=id).first()
        if goluse is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(goluse)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        golusema_update = Golusemas.query.filter_by(golusemas_id=id).first()
        data = request.get_json()

        if 'nome' in data:
            golusema_update.nome = data['nome']
        elif 'unidade' in data:
            golusema_update.unidade = data['unidade']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(golusema_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para Sabor  method get put post delete
"""


class Sabores(Resource):

    @token_required
    def get(self):
        sabor = Sabor.query.all()
        return jsonify({
            "sabor": [sab.to_dict()for sab in sabor]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            sabor = Sabor(nome=data['nome'],
                          descricao_sabor=data['descricao_sabor'])
            db.sesssion.add(sabor)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"
        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self,id):
        
        sabor = Sabor.query.filter_by(venda_id=id).first()
        if sabor is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(sabor)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        sabor_update = Sabor.query.filter_by(sabor_id=id).first()
        data = request.get_json()

        if 'nome' in data:
            sabor_update.nome = data['nome']
        elif 'descricao_sabor' in data:
            sabor_update.descricao_sabor = data['descricao_sabor']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(sabor_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


"""
Routa para Caldas  method get put post delete
"""


class Caldas(Resource):

    @token_required
    def get(self):
        calda = Calda.query.all()
        return jsonify({
            "calda": [cald.to_dict() for cald in calda]
        })

    @token_required
    def post(self):
        message_error = ""
        data = request.get_json()
        try:
            calda = Calda(nome=data['nome'],
                          descricao_calda=data['descricao_calda'])
            db.session.add(calda)
            db.session.commit()
            message_error = "1"
        except Exception:
            message_error = "4743"

        return jsonify({
            "message_error": message_error
        })

    @token_required
    def delete(self):
        data = request.get_josn()
        if data['id'] == "":
            jsonify({"message_error": "user not found"})
        calda = Calda.query.filter_by(venda_id=id).first()
        if calda is None:
            jsonify({"message_error": "user not found"})
        try:
            db.session.delete(calda)
            db.session.commit()
            return jsonify({"message_error": "user not found"})
        except Exception:
            jsonify({"message_error": "user not found"})

    @token_required
    def put(self, id):
        calda_update = Calda.query.filter_by(calda_id=id).first()
        data = request.get_json()

        if 'nome' in data:
            calda_update.nome = data['nome']
        elif 'descricao_calda' in data:
            calda_update.descricao_calda = data['descricao_calda']
        else:
            return jsonify({
                "msg": "msg"
            })
        try:
            db.session.add(calda_update)
            db.session.commit()
        except Exception:
            return jsonify({
                "msg": "msg"
            })


""" 
Routa para buscar produto   method post
"""


class SearchProduto(Resource):

    @token_required
    def post(self):
        data = request.get_json()

        if 's_produto' in data:
            produto_search = Produto.query.filter_by(
                produto_nome=data['s_produto']).first()

            return jsonify({
                "produtos": [produto.to_dict() for produto in produto_search]
            })


"""
Routa para buscar venda  method  post
"""


class SearchVenda(Resource):

    @token_required
    def post(self):
        data = request.get_json()
        if 'data' in data:
            s_venda = Venda.query.filter_by(data=data['data']).first()

            return jsonify({
                "venda_id":s_venda.venda_id,
                "data":str(s_venda.data),
                "pedido_id":s_venda.pedidovenda_id,
                "usuario_id":s_venda.usuario_id,
                "valor":s_venda.valor 
            })


"""
Routa para buscar pedido_venda  method post
"""


class SearchPedidoVenda(Resource):

    
    def post(self):
        data = request.get_json()
        if 'data' in data:
            s_pedido_venda = PedidoVenda.query.filter_by(
                data=data['data']).join(Venda, PedidoVenda == Venda.venda_id).all()
            return jsonify({
                "pedidovenda":[pdv.to_dict() for pdv in s_pedido_venda]
            })
            """
            return jsonify({
               "pedidovenda_id":s_pedido_venda.pedidovenda_id,
               "data":str(s_pedido_venda.data),
               "quantidade":s_pedido_venda.quantidade,
               "total":s_pedido_venda.total,
               "itenspedidovenda":s_pedido_venda.itensPedidoVenda
            })
            """
""" 
Routa para buscar sabor 
""" 

class SearchSabor(Resource):
    
    def post(self): 
        data = request.get_json() 
        sabor = Sabor.query.filter_by(nome=data['nome']).first() 
        return jsonify({
            "sabor_id":sabor.sabor_id,
            "nome":sabor.nome,
            "descricao_sabor":sabor.descricao_sabor
        })

""" 
Routa para buscar  categoria 
"""        

class SearchCategoria(Resource):
    
    def post(self):
        data = request.get_json()
        categoria = Categoria.query.filter_by(nome=data['nome']).first()
        return jsonify({
            "categoria_id":categoria.categoria_id,
            "nome":categoria.nome
            
        })
        
"""
Routa para buscar golusemas 
"""     


class SearchGoluma(Resource): 
    
    def post(self):
        data = request.get_json()
        gol = Golosemas.query.fiter_by(nome=data['nome']).first()
        return jsonify({
            "golusemas_id":gol.golusemas_id,
            "nome":gol.nome,
            "unidade":gol.unidade
        })