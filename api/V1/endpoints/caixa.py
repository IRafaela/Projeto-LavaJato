from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date, datetime 

from models.caixa_model import CaixaModel
from schemas.caixa_schema import CaixaSchema, CaixaSchemaCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session


router = APIRouter()

@router.get('/')
async def listar_transacoes(
    data: date = None,
    db: AsyncSession = Depends(get_session)
):
    data_alvo = data or date.today()

    inicio_dia = datetime.combine(data_alvo, datetime.min.time())
    fim_dia = datetime.combine(data_alvo, datetime.max.time())

    query = select(CaixaModel).where (
        CaixaModel.data_hora >= inicio_dia, CaixaModel.data_hora <= fim_dia
    )
    
    result = await db.execute(query)
    transacoes = result.scalars().all()

    return transacoes


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CaixaSchema)
async def criar_transacao(transacao: CaixaSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_registro = CaixaModel(
        tipo=transacao.tipo,
        descricao=transacao.descricao,
        valor=transacao.valor,
        forma_pagamento=transacao.forma_pagamento,
        data_hora=datetime.now()
    )
    db.add(novo_registro)
    await db.commit()
    await db.refresh(novo_registro)

    return novo_registro