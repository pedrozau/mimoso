from vite.extension.database import db 
from sqlalchemy_serializer import SerializerMixin


class User(db.Model,SerializerMixin):
    usuario_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(30),unique=True)
    senha = db.Column(db.String(250),nullable=False) 
    foto = db.Column(db.String(30),nullable=False)
    tipo_usuario = db.Column(db.String(30),nullable=False) 
    token = db.Column(db.String(300),nullable=False) 
     
    
    
    
class PedidoVenda(db.Model,SerializerMixin):
    pedidovenda_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    data = db.Column(db.DateTime,nullable=False)
    quantidade = db.Column(db.Integer,nullable=False)
    total = db.Column(db.Integer,nullable=False)
   
    
    
class Venda(db.Model,SerializerMixin):
    venda_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    data = db.Column(db.DateTime,nullable=False)
    pedidovenda_id = db.Column(db.Integer,db.ForeignKey("pedido_venda.pedidovenda_id"))
    usuario_id = db.Column(db.Integer,db.ForeignKey("user.usuario_id"))
    valor = db.Column(db.Integer,nullable=False)
    
    
    

class AbrirCaixa(db.Model, SerializerMixin):
    abrircaixa_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    sumplemento = db.Column(db.Integer,nullable=False)
    despsas = db.Column(db.Integer,nullable=False)
    valorInicial = db.Column(db.Integer,nullable=False)
    dataAbertura = db.Column(db.DateTime,nullable=False)
    usuario_id = db.Column(db.Integer,db.ForeignKey("user.usuario_id"))
    total = db.Column(db.Integer,nullable=False)
    
    

class FecharCaixa(db.Model, SerializerMixin):
    fecharcaixa_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    despsas = db.Column(db.Integer,nullable=False)
    dataFechamento = db.Column(db.DateTime,nullable=False)
    usuario_id = db.Column(db.Integer,db.ForeignKey("user.usuario_id"))
    total = db.Column(db.Integer,nullable=False)
    


class Categoria(db.Model, SerializerMixin):
    categoria_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(30),nullable=False)
   

class Golusemas(db.Model, SerializerMixin):
    golusemas_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(30),nullable=False)
    unidade = db.Column(db.String(10),nullable=False)
    

class Sabor(db.Model, SerializerMixin):
    sabor_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(30),nullable=False)
    descricao_sabor = db.Column(db.Text,nullable=False)
    

class Calda(db.Model, SerializerMixin):
    calda_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String(30),nullable=False)
    descricao_calda = db.Column(db.Text,nullable=False)
    
 
 
    
class Produto(db.Model,SerializerMixin):
    produto_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    produto_nome = db.Column(db.String(30),nullable=False)
    preco = db.Column(db.Integer,nullable=False)
    descricao_produto = db.Column(db.Text,nullable=False)
    unidade = db.Column(db.String(10),nullable=False)
    categoria_id = db.Column(db.Integer,db.ForeignKey("categoria.categoria_id"))
    sabor_id = db.Column(db.Integer,db.ForeignKey("sabor.sabor_id"))
    calda_id = db.Column(db.Integer,db.ForeignKey("calda.calda_id"))
    golusemas_id = db.Column(db.Integer,db.ForeignKey("golusemas.golusemas_id"))
     
class ItensPedidoVenda(db.Model,SerializerMixin):
    itenspedidovenda_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    produto_id = db.Column(db.Integer,db.ForeignKey("produto.produto_id"))
    quantidade = db.Column(db.Integer)
    pedidodvenda_id = db.Column(db.Integer,db.ForeignKey("pedido_venda.pedidovenda_id"))