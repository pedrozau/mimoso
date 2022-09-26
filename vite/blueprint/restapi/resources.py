from dynaconf import settings
from flask import jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_restful import Resource
from markupsafe import escape

from vite.extension.token import generate_token, token_required
from vite.model import (Caixa, Calda, Categoria, FecharCaixa, Golusemas, Itens,
                        Pedido, Produto, Sabor, User, Venda, db)


class Login(Resource):
    """
    Routa para login está route permitem para todos usuarios logar no sistema.
    Com seguinte method post.
    """

    def remove_space(self, value):
        return value.replace(' ', '')

    def post(self):
        """Routa login para todos usuario do sistema só tem method post."""
        data = request.get_json()
        message_error = '' 
        if data is not 'email' and data is not 'senha':
            message_error = "Não informaste os campos em formato json: email,senha"
        else:
            if data['email'] != '' and data['senha'] != '':
                data_login = User.query.filter_by(
                    email=escape(self.remove_space(data['email']))
                ).first()

                if data_login is None:
                    message_error = 'usuario não existe'
                elif check_password_hash(
                    data_login.senha, escape(self.remove_space(data['senha']))
                ):
                    try:
                        data_login.token = generate_token(data_login.email)
                        db.session.add(data_login)
                        db.session.commit()

                    except Exception:
                        message_error = 'error ao logar'
                    return jsonify(
                        {
                            'id': data_login.id,
                            'nome': data_login.nome,
                            'email': data_login.email,
                            'senha': data_login.senha,
                            'token': data_login.token,
                            'tipo_usuario': data_login.tipo_usuario,
                        }
                    )
                else:
                    message_error = 'a tua senha está incorreta tenta novamente'
            else:
                message_error = 'Campos json email,senha'

        return jsonify({'message_error': message_error})


class Logout(Resource):
    """
    Está routa poderia usar-se para logout de usuario no sistema.
    Mas de momento ainda não tem codigo por que o logout será.
    Feito no frent-end.
    """


class Usuario(Resource):
    """
    Está routa permite list os usuario e cadastrar no sistema.
    Delete usuario,alteração dos dados dos usuario.
    """

    @token_required
    def get(self):

        user = (
            db.session.query(User, Venda, Caixa)
            .with_entities(
                User.id,
                User.nome,
                User.email,
                User.senha,
                User.foto,
                User.token,
                User.tipo_usuario,
            )
            .all()
        )

        return jsonify({'users': [dict(row) for row in user]})

    def remove_space(self, value):
        return value.replace(' ', '')

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        password_hash = generate_password_hash(
            self.remove_space(data['senha']), 15
        ).decode('utf-8')
        url = f"{settings.get('HTTP_HOST')}/static/image/user.png"
        print(url)
        token = generate_token(data['email'])

        try:
            user = User(
                nome=data['nome'],
                email=self.remove_space(data['email']),
                senha=password_hash,
                foto=url,
                tipo_usuario=data['tipo_usuario'],
                token=token,
            )
            db.session.add(user)
            db.session.commit()
            message_error = 'o usuario foi cadastrado com sucesso'
        except Exception as error:
            print(error)
            message_error = (
                f"já existe usuario cadastrado com esse nome {data['nome']} "
            )

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, usuario_id):
        message_error = ''
        if usuario_id is None:
            message_error = 'id não foi informado'

        user = User.query.filter_by(id=usuario_id).first()

        if user is None:
            message_error = 'O usuario não foi encontrado'
        else:
            try:
                db.session.delete(user)
                db.session.commit()
                message_error = 'O usuario foi deletado com sucesso'
            except Exception:
                message_error = 'O usuario não foi deletado com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, usuario_id):
        message_error = ''
        if usuario_id is None:
            message_error = 'Não informou usuario_id'
        else:
            user_update = User.query.filter_by(usuario_id=usuario_id).first()
            data = request.get_json()
            # file = request.files['foto']
            if 'nome' in data:
                user_update.nome = data['nome']
            elif 'email' in data:
                user_update.email = data['email']
            elif 'senha' in data:
                password_hash = generate_password_hash(data['senha'], 15).decode(
                    'utf-8'
                )
                user_update.senha = password_hash
            elif 'foto' in data:
                user_update.url = data['foto']
            elif 'tipo_usuario' in data:
                user_update.tipo_usuario = data['tipo_usuario']
            else:
                message_error= 'os campos estão vazio'
            try:
                db.session.add(user_update)
                db.session.commit()
                db.session.close()
                message_error = 'atualizou com sucesso'
            except Exception as error:
                message_error = f'Não atualizou com sucesso {error}'

        return jsonify({
                    "message_error": message_error
                })  
                    
""" 
Routa para ulpad de arquivos de image de usuario 
"""            
class UploadFile(Resource):
    
    def post(self):
        """
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("your_file_name.jpg")
        parse = reqparse.RquestParser() 
        parse.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file =  args['file']
        image_file = secure_filename(image_file.filename)
        image_file.save(f"../../../static/{image_file}")
         
        """
        return jsonify({
              "message_error":"message"
          })
         
        
           

"""
Routa para vendas  method get put post delete
"""



class Vendas(Resource):
    """
    Routa para listar venda e cadastrar as vendas alteração das vendas e deletar vendas.
    """

    @token_required
    def get(self):

        vendas = (
            db.session.query(Venda, User, Pedido)
            .with_entities(
                Venda.id, Venda.cliente, Venda.usuario_id, Venda.data_venda
            )
            .all()
        )
        return jsonify({'vendas': [dict(row) for row in vendas]})

    @token_required
    def post(self):

        data = request.get_json()
        message_error = ''

        if (
            'cliente' not in data
            or 'usuario_id' not in data
            or 'data_venda' not in data
        ):
            message_error = 'informe: cliente,usuario_id,data_venda'
        else:
            try:
                vendas = Venda(
                    cliente=data['cliente'],
                    usuario_id=data['usuario_id'],
                    data_venda=data['data_venda'],
                )
                db.session.add(vendas)
                db.session.commit()
                db.session.close()
                message_error = 'cadastrou com sucesso'
            except Exception as error:
                message_error = f'não cadastrou com sucesso  {error}'

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, venda_id):
        message_error = ''
        if venda_id is None:
            message_error = 'venda_id não foi informado'
        else:
            venda = Venda.query.filter_by(id=venda_id).first()
            if venda is None:
                message_error = 'não foi econtrados as  vendas'
            try:
                db.session.delete(venda)
                db.session.commit()
                db.session.close()
                message_error = 'venda foi deletado com sucesso'
            except Exception as error:
                message_error = f'venda não foi deletado com sucesso {error}'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, venda_id):
        message_error = ''
        if venda_id is None:
            message_error = 'venda_id não foi informado'
        else:
            data = request.get_json()
            venda_update = Venda.query.filter_by(id=id).first()

            if 'cliente' in data:
                venda_update.cliente = data['cliente']
            elif 'usuario_id' in data:
                venda_update.usuario_id = data['usuario_id']
            elif 'data_venda ' in data:
                venda_update.data_venda = data['venda_data']
            else:
                message_error = 'informe cliente,usuario_id,data_venda'

            try:
                db.session.add(venda_update)
                db.session.commit()
                message_error = 'Atualizou com sucesso'
            except Exception as error:
                message_error = f'Não atualizou com sucesso {error}'

        return jsonify({'message_error': message_error})


class FecharCaixas(Resource):
    """
    Routa para Fecharcaixa  method get put post delete.
    """

    @token_required
    def get(self):
        fecharcaixa = FecharCaixa.query.all()
        return jsonify(
            {
                'fechar_caixa': [
                    fechcaixa.to_dict() for fechcaixa in fecharcaixa
                ]
            }
        )

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            fecharcaixa = FecharCaixa(
                despesa=data['despesa'],
                dataFechamento=data['data_fechamento'],
                usuario_id=data['usuario_id'],
                total=data['total'],
            )
            db.session.add(fecharcaixa)
            db.session.commit()

            message_error = 'cadastrado com sucesso'
        except Exception:
            message_error = 'não cadastrado com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, fechar_id):
        message_error = ''
        if fechar_id is None:
            message_error = 'fechar_id não foi informado'
        else:
            fecharcaixa = FecharCaixa.query.filter_by(
                fecharcaixa_id=fechar_id
            ).first()
            if fecharcaixa is None:
                message_error = 'não foi encontrado'
            try:
                db.session.delete(fecharcaixa)
                db.session.commit()
                message_error = 'cadastrou com sucesso'
            except Exception as error:
                message_error = f'não cadastrou com sucesso {error}'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, fechar_id):
        message_error = ''
        if fechar_id is None:
            message_error = 'Não foi informado fechar_id'
        else:

            fcaixa_update = FecharCaixa.query.filter_by(
                fecharcaixa_id=fechar_id
            ).first()
            data = request.get_json()

            if 'despesa' in data:
                fcaixa_update.despesa = data['despesa']
            elif 'data_fechamneto' in data:
                fcaixa_update.dataFechamento = data['data_fechamento']
            elif 'usuario_id' in data:
                fcaixa_update.usuario_id = data['usuario_id']
            elif 'total' in data:
                fcaixa_update.total = data['total']
            else:
                message_error = 'não informou os dados'
            try:
                db.session.add(fcaixa_update)
                db.session.commit()
                message_error = 'atualizou com sucesso'
            except Exception as error:
                message_error = f'não atualizou com sucesso {error}'

        return jsonify({'message_error': message_error})


class Pedidos(Resource):
    """
    Routa para PedidoVenda  method get put post delete.
    """

    @token_required
    def get(self):

        pedidovenda = (
            db.session.query(Pedido, Venda)
            .join(Venda, Pedido.venda_id == Venda.id)
            .with_entities(
                Pedido.id,
                Pedido.data,
                Pedido.quantidade,
                Pedido.total,
                Pedido.venda_id,
            )
        )
        return jsonify({'pedido': [dict(row) for row in pedidovenda]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            pvenda = Pedido(
                data=data['data'],
                quantidade=data['quantidade'],
                total=data['total'],
                venda_id=data['venda_id'],
            )
            db.session.add(pvenda)
            db.session.commit()
            message_error = 'cadastrou com sucessso'
        except Exception as error:
            print(error)
            message_error = 'não cadastro com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, pedido_id):
        message_error = ''
        if pedido_id is None:
            message_error = 'pedido_id não foi informado'
        else:

            pedidovenda = Pedido.query.filter_by(id=pedido_id).first()
            if pedidovenda is None:
                message_error = 'não foi encontrado'
            try:
                db.session.delete(pedidovenda)
                db.session.commit()
                message_error = 'cadastrou com sucesso'
            except Exception as error:
                message_error = f'não cadastrou com sucesso {error}'
        return jsonify({'message_error': message_error})

    @token_required
    def put(self, pedido_id):
        message_error = ''
        if pedido_id is None:
            message_error = 'pedido_id não foi informado'
        else:
            pv_update = Pedido.query.filter_by(id=pedido_id).first()
            data = request.get_json()

            if 'data' in data:
                pv_update.data = data['data']
            elif 'quantidade' in data:
                pv_update.quantidade = data['quantidade']
            elif 'total' in data:
                pv_update.total = data['total']
            elif 'venda_id' in data:
                pv_update.venda_id = data['venda_id']
            else:
                message_error = 'não informou os dados'
            try:
                db.session.add(pv_update)
                db.session.commit()
                message_error = 'atualizou com sucesso'
            except Exception as error:
                message_error = f'não atuaçizou com sucesso {error}'
        return jsonify({'message_error': message_error})


class Items(Resource):

    """
    Routa para ItensPedidoVendas   method get put post delete.
    """

    @token_required
    def get(self):

        items = db.session.query(Itens, Pedido).with_entities().all()
        return jsonify({'items': [itens.to_dict() for itens in items]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            itens = Itens(
                quantidade=data['quantidade'], total_itens=data['total_itens']
            )
            db.session.add(itens)
            db.session.commit()
            message_error = 'cadastrou com sucesso'
        except Exception as error:
            message_error = f'Não cadastrou com sucesso {error}'
        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, itens_id):
        message_error = ''
        if itens_id is None:
            message_error = 'Não foi informado itens_id'
        else:
            itens = Itens.query.filter_by(id=itens_id).first()
            if itens is None:
                message_error = 'usuario não econtrado'
            try:
                db.session.delete(itens)
                db.session.commit()
                message_error = 'cadastrou com sucesso'
            except Exception:
                message_error = 'Não cadastrou com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, itens_id):
        message_error = ''
        if itens_id is None:
            message_error = 'Não foi informado itens_id'
        else:
            itpv_update = Itens.query.filter_by(id=itens_id).first()
            data = request.get_json()

            if 'produto_id' in data:
                itpv_update.produto_id = data['produto_id']
            elif 'quantidade' in data:
                itpv_update.quantidade = data['quantidade']
            elif 'total_itens' in data:
                itpv_update.total_itens = data['total_itens']
            else:
                message_error = 'não informou os dados'
            try:
                db.session.add(itpv_update)
                db.session.commit()
                message_error = 'atualizou com sucesso'
            except Exception:
                message_error = 'não atualizou com sucesso'

        return jsonify({'message_error': message_error})


class Produtos(Resource):
    """
    Routa para Lista todos produto  method get put post delete.
    """

    @token_required
    def get(self):

        produto = (
            db.session.query(Produto)
            .with_entities(
                Produto.produto_id,
                Produto.produto_nome,
                Produto.preco,
                Produto.descricao_produto,
                Produto.unidade,
                Produto.itens_id,
            )
            .all()
        )
        return jsonify({'produto': [dict(row) for row in produto]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            prod = Produto(
                produto_nome=data['produto_nome'],
                preco=data['preco'],
                descricao_produto=data['descricao_produto'],
                unidade=data['unidade'],
                itens_id=data['itens_id'],
            )
            db.session.add(prod)
            db.session.commit()
            message_error = 'cadastrou  com sucesso'
        except Exception:
            message_error = 'não cadastrou com sucesso'
        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, produto_id):
        message_error = ''
        if produto_id is None:
            message_error = 'Não foi informado produto_id'
        else:
            prod = Produto.query.filter_by(produto_id=produto_id).first()
            if prod is None:
                message_error = 'Produto não foi encontrado'
            try:
                db.session.delete(prod)
                db.session.commit()
                message_error = 'cadastrou com sucesso'
            except Exception:
                message_error = 'Não cadastrou com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, produto_id):
        produto_update = Produto.query.filter_by(produto_id=produto_id).first()
        data = request.get_json()

        if 'produto_nome' in data:
            produto_update.produto_nome = data['produto_nome']
        elif 'preco' in data:
            produto_update.preco = data['preco']
        elif 'descricao_produto' in data:
            produto_update.descricao_produto = data['descricao_produto']
        elif 'unidade' in data:
            produto_update.unidade = data['unidade']

        elif 'itens_id' in data:
            produto_update.itens_id = data['itens_id']
        else:
            return jsonify({'message_error': 'não informou os dados'})
        try:
            db.session.add(produto_update)
            db.session.commit()
            return jsonify({'message_error': 'atualizou com sucesso'})
        except Exception:
            return jsonify({'message_error': 'não atualizou com sucesso'})


class Categorias(Resource):
    """
    Routa para Categoria   method get put post delete.
    """

    # @token_required
    def get(self):
        categoria = Categoria.query.all()
        return jsonify({'categoria': [cat.to_dict() for cat in categoria]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            categoria = Categoria(nome=data['nome'])
            db.session.add(categoria)
            db.session.commit()
            message_error = 'cadastrou com sucesso'
        except Exception:
            message_error = 'não cadastrou com sucesso'
        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, categoria_id):
        message_error = ''
        if categoria_id is None:
            message_error = 'Não foi informado categoria_id'
        else:
            categoria = Categoria.query.filter_by(
                categoria_id=categoria_id
            ).first()
            if categoria is None:
                message_error = 'categoria não em encontrado'
            try:
                db.session.delete(categoria)
                db.session.commit()
                message_error = 'cadastrou com sucesso'
            except Exception:
                message_error = 'Não cadastrou com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, categoria_id):

        message_error = ''
        if categoria_id is None:
            message_error = 'Não foi informado categoria_id'
        else:
            categoria_update = Categoria.query.filter_by(
                categoria_id=categoria_id
            ).first()
            data = request.get_json()

            if 'nome' in data:
                categoria_update.nome = data['nome']
            else:
                message_error = 'não informou os dados '
            try:
                db.session.add(categoria_update)
                db.session.commit()
                message_error = 'atualizou com sucesso'
            except Exception:
                message_error = 'não atualizou com sucesso'
        return jsonify({'message_error': message_error})


class Golusemase(Resource):
    """
    Routa para Golusemase  method get put post delete.
    """

    @token_required
    def get(self):
        golusemas = Golusemas.query.all()
        return jsonify(
            {'golusemas': [golese.to_dict() for golese in golusemas]}
        )

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            golusemas = Golusemas(nome=data['nome'], unidade=data['unidade'])
            db.session.add(golusemas)
            db.session.commit()
            message_error = 'cadastrou com sucesso'
        except Exception:
            message_error = 'não cadasrou com sucesso'

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, golusemas_id):
        message_error = ''
        if golusemas_id is None:
            message_error = 'Não foi informado golusemas_id'
        else:
            goluse = Golusemas.query.filter_by(
                golusemas_id=golusemas_id
            ).first()
            if goluse is None:
                message_error = 'usuario não existe no sistema'
            try:
                db.session.delete(goluse)
                db.session.commit()
                message_error = 'deletou com sucesso'
            except Exception:
                message_error = 'Não deletou com sucesso'
        return jsonify({'message_error': message_error})

    @token_required
    def put(self, golusemas_id):
        message_error = ''
        if golusemas_id is None:
            message_error = 'Não foi informado golusemas_id'
        else:
            golusema_update = Golusemas.query.filter_by(
                golusemas_id=golusemas_id
            ).first()
            data = request.get_json()

            if 'nome' in data:
                golusema_update.nome = data['nome']
            elif 'unidade' in data:
                golusema_update.unidade = data['unidade']
            else:
                message_error = 'não informou os dados'
            try:
                db.session.add(golusema_update)
                db.session.commit()
                message_error = 'atualizou com sucesso'
            except Exception:
                message_error = 'não atualizou com sucesso'
        return jsonify({'message_error': message_error})


class Sabores(Resource):
    """
    Routa para Sabor  method get put post delete.
    """

    @token_required
    def get(self):
        sabor = Sabor.query.all()
        return jsonify({'sabor': [sab.to_dict() for sab in sabor]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            sabor = Sabor(
                nome=data['nome'], descricao_sabor=data['descricao_sabor']
            )
            db.sesssion.add(sabor)
            db.session.commit()
            message_error = 'cadastrou com sucesso'
        except Exception:
            message_error = 'não cadastrou com sucesso'
        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, sabor_id):

        sabor = Sabor.query.filter_by(sabor_id=sabor_id).first()
        if sabor is None:
            jsonify({'message_error': 'não foi econtrado'})
        try:
            db.session.delete(sabor)
            db.session.commit()
            return jsonify({'message_error': 'deletou com sucesso'})
        except Exception:
            jsonify({'message_error': 'não deletou com sucesso'})

        return jsonify({'message_error': 'message_error'})

    @token_required
    def put(self, sabor_id):
        sabor_update = Sabor.query.filter_by(sabor_id=sabor_id).first()
        data = request.get_json()

        if 'nome' in data:
            sabor_update.nome = data['nome']
        elif 'descricao_sabor' in data:
            sabor_update.descricao_sabor = data['descricao_sabor']
        else:
            return jsonify({'message_error': 'não informou os dados'})
        try:
            db.session.add(sabor_update)
            db.session.commit()
            return jsonify({'message_error': 'atualizou com sucesso'})
        except Exception:
            return jsonify({'message_error': 'Não atualizou com sucesso'})

        return jsonify({'message_error': 'message_error'})


class Caldas(Resource):
    """
    Routa para Caldas  method get put post delete.
    """

    @token_required
    def get(self):
        calda = Calda.query.all()
        return jsonify({'calda': [cald.to_dict() for cald in calda]})

    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        try:
            calda = Calda(
                nome=data['nome'], descricao_calda=data['descricao_calda']
            )
            db.session.add(calda)
            db.session.commit()
            message_error = '1'
        except Exception:
            message_error = '4743'

        return jsonify({'message_error': message_error})

    @token_required
    def delete(self, calda_id):

        calda = Calda.query.filter_by(calda_id=calda_id).first()
        if calda is None:
            jsonify({'message_error': 'user not found'})
        try:
            db.session.delete(calda)
            db.session.commit()
            return jsonify({'message_error': 'user not found'})
        except Exception:
            jsonify({'message_error': 'user not found'})
        return jsonify({'message_error': 'message_error'})

    @token_required
    def put(self, calda_id):
        calda_update = Calda.query.filter_by(calda_id=calda_id).first()
        data = request.get_json()

        if 'nome' in data:
            calda_update.nome = data['nome']
        elif 'descricao_calda' in data:
            calda_update.descricao_calda = data['descricao_calda']
        else:
            return jsonify({'msg': 'msg'})
        try:
            db.session.add(calda_update)
            db.session.commit()
            return jsonify({'message_error': 'atualizou com sucesso'})
        except Exception:
            return jsonify({'message_error': 'não cadastro com sucesso'})
        return jsonify({'message_error': 'message_error'})


class Caixas(Resource):
    """
    Routa para  Caixa get,post,put, delete.
    """
    @token_required
    def get(self):
        caixa = (
            db.session.query(Caixa,FecharCaixa)
            .with_entities(
                Caixa.id,
                Caixa.usuario_id,
                Caixa.data_caixa,
                Caixa.suplemento,
                Caixa.total_caixa,
            )
            .all()
        )
        return jsonify({'caixa': [dict(row) for row in caixa]})
    @token_required
    def post(self):
        message_error = ''
        data = request.get_json()
        if (
            'usuario_id' not in data
            or 'data_caixa' not in data
            or 'suplemento' not in data
            or 'total_caixa' not in data
        ):
            message_error = (
                'informe: usuario_id,data_caixa,suplemento,total_caixa'
            )
        else:
            try:
                total_valor = int(data['suplemento']) + int(
                    data['total_caixa']
                )
                caixa_add = Caixa(
                    usuario_id=data['usuario_id'],
                    data_caixa=data['data_caixa'],
                    suplemento=data['suplemento'],
                    total_caixa=total_valor,
                )
                db.session.add(caixa_add)
                db.session.commit()
                db.session.close()
                message_error = 'cadastrou com sucesso'

            except Exception as error:
                print(f'message: [{error}]')
                message_error = f'não cadastrou com sucesso {error}'

        return jsonify({'message_error': message_error})

    @token_required
    def put(self, caixa_id):
        message_error = ''
        data = request.get_json()
        caixa_update = Caixa.query.filter_by(id=caixa_id).first()

        if 'usuario_id' in data:
            caixa_update.usuario_id = data['usuario_id']
        elif 'data_caixa' in data:
            caixa_update.data_caixa = data['data_caixa']
        elif 'suplemento' in data:
            caixa_update.suplemento = data['suplemento']
            total_valor = int(caixa_update.total_caixa) + int(
                data['suplemento']
            )
            caixa_update.total_caixa = total_valor

        elif 'total_caixa' in data:

            caixa_update.total_caixa = int(data['total_caixa'])
        else:
            message_error = (
                'informe: usuario_id,data_caixa,suplemento,total_caixa'
            )
        try:
            db.session.add(caixa_update)
            db.session.commit()
            db.session.close()
            message_error = 'Atualizou com sucesso '
        except Exception as error:
            message_error = f'Não atualizou com sucesso {error}'
        return jsonify({'message_error': message_error})
    @token_required
    def delete(self, caixa_id):
        message_error = ''
        caixa = Caixa.query.filter_by(id=caixa_id).first()
        if caixa is None:
            message_error = 'Não encontrada'
        else:
            try:
                db.session.delete(caixa)
                db.session.commit()

                message_error = 'deletou com sucesso'
            except Exception as error:
                message_error = f'Não deletou com sucesso {error}'

        return jsonify({'message_error': message_error})


class SearchProduto(Resource):
    """
    Routa para buscar produto   method post.
    """

    @token_required
    def post(self):
        data = request.get_json()

        if 's_produto' in data:
            produto_search = Produto.query.filter_by(
                produto_nome=data['s_produto']
            ).first()

        return jsonify(
            {'produtos': [produto.to_dict() for produto in produto_search]}
        )


class SearchVenda(Resource):
    """
    Routa Para procurar as venda no sistema methods post.
    """

    @token_required
    def post(self):
        data = request.get_json()
        if 'data' in data:
            s_venda = Venda.query.filter_by(data=data['data']).first()

        return jsonify(
            {
                'venda_id': s_venda.venda_id,
                'data': str(s_venda.data),
                'pedido_id': s_venda.pedidovenda_id,
                'usuario_id': s_venda.usuario_id,
                'valor': s_venda.valor,
            }
        )


class SearchPedidoVenda(Resource):
    """
    Routa para buscar pedido_venda  method post.
    """

    def post(self):
        data = request.get_json()
        if 'data' in data:
            s_pedido_venda = (
                Pedido.query.filter_by(data=data['data'])
                .join(Venda, Pedido == Venda.venda_id)
                .all()
            )
        return jsonify(
            {'pedidovenda': [pdv.to_dict() for pdv in s_pedido_venda]}
        )


class SearchSabor(Resource):
    """
    Routa para procurar  sabor no sistema.
    """
    @token_required
    def post(self):
        data = request.get_json()
        sabor = Sabor.query.filter_by(nome=data['nome']).first()
        return jsonify(
            {
                'sabor_id': sabor.sabor_id,
                'nome': sabor.nome,
                'descricao_sabor': sabor.descricao_sabor,
            }
        )


class SearchCategoria(Resource):

    """
    Routa para procurar as  categoria no sistema.
    """
    @token_required
    def post(self):
        data = request.get_json()
        categoria = Categoria.query.filter_by(nome=data['nome']).first()
        return jsonify(
            {'categoria_id': categoria.categoria_id, 'nome': categoria.nome}
        )


class SearchGoluma(Resource):
    """
    Routa para procurar  golusemas no sistema pelo  seu nome.
    """
    @token_required
    def post(self):
        data = request.get_json()
        gol = Golusemas.query.fiter_by(nome=data['nome']).first()
        return jsonify(
            {
                'golusemas_id': gol.golusemas_id,
                'nome': gol.nome,
                'unidade': gol.unidade,
            }
        )

class Relatorio(Resource):
    
    @token_required
    def get(self):
        """
           Routa para relatorio de Venda efetuada no sistema.
           Return relatorio mensal,trimenstrial, anoal 
        """
        message_error = ''
        data = request.get_json()
        
        if data is not 'data_inicial' or  data is not 'data_final':
            if data['data_inicial'] != "" or data['data_final'] != "":
                report = db.session.query(Venda,User,Pedido).filter(Venda.data_venda.between(data['data_inicial'],data['data_final'])).with_entities(
                
                    Venda.cliente,
                    Venda.data_venda,
                    Pedido.quantidade,
                    Pedido.total,
                
                ).all()
                return jsonify({'Report':[dict(venda) for venda in report]})
            else:
                message_error = "Campos vazio"
        else: 
            message_error = 'informe data_inicial:2022-01-01,data_final:2022-02-28'

        return jsonify({'message_error':message_error})
