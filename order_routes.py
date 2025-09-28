from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def orders():
    """
    Rota padrao order
    """
    return {"mensagem": "Voce acessou"}

@order_router.post("/pedido")
async def orders(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Rota para criar um pedido
    """
    novo_Pedido = Pedido(usuario=pedido_schema.id_usuario, status=pedido_schema.status, preco=pedido_schema.preco)
    session.add(novo_Pedido)
    session.commit()
    return {"Mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_Pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if pedido.usuario != usuario.id or not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para cancelar este pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "Mensagem": f"Pedido {pedido.id} cancelado com sucesso.",
        "Pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para listar os pedidos")
    else:
        pedidos = session.query(Pedido).all()
        return {"Pedidos": pedidos}
    
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int , item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if pedido.usuario != usuario.id or not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para adicionar itens a este pedido")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {"Mensagem": f"Item adicionado ao pedido {id_pedido} com sucesso."
            , "Item": item_pedido
            , "Preco total do pedido": pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def adicionar_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.id_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="item no pedido nao encontrado")
    if pedido.usuario != usuario.id or not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para adicionar itens a este pedido")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {"Mensagem": f"Item removido com sucesso com sucesso."
            , "Quandtidade_itens_pedido": len(pedido.itens)
            , "Pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if pedido.usuario != usuario.id or not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para cancelar este pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "Mensagem": f"Pedido {pedido.id} cancelado com sucesso.",
        "Pedido": pedido
    }

@order_router.get("/pedido/{id_pedido}")
async def detalhar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if pedido.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=401, detail="Voce nao tem permissao para ver os detalhes deste pedido")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "Pedido": pedido
    }

@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos
    