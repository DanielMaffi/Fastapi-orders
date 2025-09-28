from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///database/banco.db")

Base = declarative_base()

# ========================= #

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    nome = Column("nome", String, nullable=True)
    email = Column("email", String, nullable=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# ========================= #

class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDITOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    #ChoiceType(choices=STATUS_PEDITOS)
    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    status = Column("status", String ,default="PENDENTE") 
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")

    def __init__(self,  usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self, itens):
        #preco_pedido = 0
        #for item in self.itens:
            #preco_item = item.preco_unitario * item.quantidade
            #preco_pedido += preco_item
            
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

# ========================= #

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, nullable=True)
    sabor = Column("sabor", String, nullable=True) 
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho 
        self.preco_unitario = preco_unitario
        self.pedido = pedido      