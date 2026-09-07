from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models.usuario_model import UsuarioModel
from models.cliente_model import ClienteModel
from schemas.cliente_schema import ClienteSchema, ClienteResponseSchema
from core.deps import get_session, get_current_user

router = APIRouter()

#Rota para cadastrar cliente
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=ClienteResponseSchema)
async def post_cliente(cliente: ClienteSchema, db: AsyncSession = Depends(get_session)):
    novo_cliente = ClienteModel(**cliente.model_dump())
  
    
    db.add(novo_cliente)
    await db.commit()

    await db.refresh(novo_cliente, attribute_names=['veiculos'])
   

    return novo_cliente

#Rota para trazer todos os clientes
@router.get('/', response_model=List[ClienteResponseSchema])
async def listar_clientes(db: AsyncSession = Depends(get_session)):
   
        query = select(ClienteModel).options(joinedload(ClienteModel.veiculos))
        result = await db.execute(query)

        clientes: List[ClienteModel] = result.scalars().unique().all()

        return clientes

#Rota para trazer um cliente especifico
@router.get('/{cliente_id}', response_model=ClienteResponseSchema, status_code=status.HTTP_200_OK)
async def get_cliente(
     cliente_id: int, 
     db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ClienteModel).options(joinedload(ClienteModel.veiculos)).filter(ClienteModel.id == cliente_id)
        result = await db.execute(query)

        cliente = result.scalars().unique().first()

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente não encontrado')
        else:
            return cliente

#Rota para atualizar um cliente
@router.put('/{cliente_id}', response_model=ClienteResponseSchema, status_code=status.HTTP_200_OK)
async def atualizar_cliente(
cliente_id: int, 
cliente_dados: ClienteSchema, db: AsyncSession = Depends(get_session),
usuario_logado: UsuarioModel = Depends(get_current_user)
):
        
        query = select(ClienteModel).options(joinedload(ClienteModel.veiculos)).filter(ClienteModel.id == cliente_id)
        result = await db.execute(query)
        cliente_up = result.scalars().unique().first()

        if not cliente_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente não encontrado')
    
        for chave, valor in cliente_dados.model_dump().items():
            setattr(cliente_up, chave, valor)

        await db.commit()
        await db.refresh(cliente_up, attribute_names=['veiculos'])
        return cliente_up


@router.delete('/{cliente_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(
    cliente_id: int, 
    db: AsyncSession = Depends(get_session), 
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
   
        query = select(ClienteModel).filter(ClienteModel.id == cliente_id)
        result = await db.execute(query)
        cliente = result.scalars().first()

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cliente não encontrado')
        
        await db.delete(cliente)
        await db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


   
