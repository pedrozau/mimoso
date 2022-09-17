from sqlalchemy_serializer import SerializerMixin

from vite.extension.database import db

association_table = db.Table(
    'association',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        nullable=False,
    ),
    db.Column(
        'venda_id',
        db.Integer,
        db.ForeignKey('venda.id'),
        primary_key=True,
        nullable=False,
    ),
    db.PrimaryKeyConstraint('user_id', 'venda_id'),
)

association_pedido = db.Table(
    'association_pedido',
    db.Column(
        'pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True
    ),
    db.Column(
        'itens_id', db.Integer, db.ForeignKey('itens.id'), primary_key=True
    ),
    db.PrimaryKeyConstraint('pedido_id', 'itens_id'),
)


class User(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True)
    senha = db.Column(db.String(250), nullable=False)
    foto = db.Column(db.String(150), nullable=False)
    tipo_usuario = db.Column(db.String(30), nullable=False)
    token = db.Column(db.String(300), nullable=False)
    venda = db.relationship(
        'Venda',
        secondary=association_table,
        lazy='joined',
        backref=db.backref('users', lazy='subquery'),
    )
    caixa = db.relationship('Caixa', backref='caixa', lazy='subquery')


class Venda(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(30), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    pedido = db.relationship('Pedido', backref='pedido', lazy='subquery')


class Caixa(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_caixa = db.Column(db.Date, nullable=False)
    suplemento = db.Column(db.Numeric, nullable=False)
    total_caixa = db.Column(db.Numeric, nullable=False)
    fechar = db.relationship('FecharCaixa', backref='caixa', lazy='subquery')


class FecharCaixa(db.Model, SerializerMixin):
    fecharcaixa_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    despesa = db.Column(db.Integer, nullable=False)
    data_fechamento = db.Column(db.DateTime, nullable=False)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixa.id'))
    total_caixa = db.Column(db.Numeric, nullable=False)


class Pedido(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'))
    pedido_venda = db.relationship(
        'Itens',
        secondary=association_pedido,
        lazy='subquery',
        backref=db.backref('pedido', lazy='subquery'),
    )


class Itens(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantidade = db.Column(db.Integer, nullable=True)
    total_itens = db.Column(db.Integer, nullable=False)
    produto = db.relationship('Produto', backref='itens', lazy=True)
    categoria = db.relationship('Categoria', backref='itens', uselist=False)
    golusema = db.relationship('Golusemas', backref='itens', uselist=False)
    sabor = db.relationship('Sabor', backref='itens', uselist=False)
    calda = db.relationship('Calda', backref='itens', uselist=False)


class Produto(db.Model, SerializerMixin):
    produto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_nome = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Numeric, nullable=False)
    descricao_produto = db.Column(db.Text, nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    itens_id = db.Column(db.Integer, db.ForeignKey('itens.id'))


class Categoria(db.Model, SerializerMixin):
    categoria_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    itens_id = db.Column(db.Integer, db.ForeignKey('itens.id'))


class Golusemas(db.Model, SerializerMixin):
    golusemas_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    unidade = db.Column(db.String(10), nullable=False)
    itens_id = db.Column(db.Integer, db.ForeignKey('itens.id'))


class Sabor(db.Model, SerializerMixin):
    sabor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao_sabor = db.Column(db.Text, nullable=False)
    itens_id = db.Column(db.Integer, db.ForeignKey('itens.id'))


class Calda(db.Model, SerializerMixin):
    calda_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao_calda = db.Column(db.Text, nullable=False)
    itens_id = db.Column(db.Integer, db.ForeignKey('itens.id'))
