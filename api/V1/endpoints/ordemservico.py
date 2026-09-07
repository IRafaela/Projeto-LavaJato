from datetime import datetime
from typing import List, Optional
from datetime import datetime, date

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.ordemservico_model import OrdemServicoModel
from models.caixa_model import CaixaModel

from schemas.ordemservico_schema import (
    OrdemServicoResponseSchema,
    OrdemServicoCreateSchema,
    OrdemEntregaSchema
)

from core.database import get_session
from core.deps import get_current_user


router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=OrdemServicoResponseSchema
)
async def criar_ordem_servico(
    payload: OrdemServicoCreateSchema,
    db: AsyncSession = Depends(get_session)
):
    nova_ordem = OrdemServicoModel(
        tipo_lavagem=payload.tipo_lavagem,
        valor=payload.valor,
        veiculo_id=payload.veiculo_id,
        funcionario_id=payload.funcionario_id
    )

    db.add(nova_ordem)
    await db.commit()
    await db.refresh(nova_ordem)

    return nova_ordem


@router.get(
    '/',
    response_model=List[OrdemServicoResponseSchema]
)
async def listar_ordens_servico(
    db: AsyncSession = Depends(get_session)
):
    resultado = await db.execute(
        select(OrdemServicoModel)
    )

    return resultado.scalars().all()


@router.get(
    '/{ordem_id}',
    response_model=OrdemServicoResponseSchema
)
async def buscar_ordem_id(
    ordem_id: int,
    db: AsyncSession = Depends(get_session)
):
    resultado = await db.execute(
        select(OrdemServicoModel).where(
            OrdemServicoModel.id == ordem_id
        )
    )

    ordem = resultado.scalar_one_or_none()

    if not ordem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ordem de serviço não encontrada.'
        )

    return ordem


# ...existing code...

@router.patch('/{ordem_id}/entrega')
async def entregar_veiculo(
    ordem_id: int,
    dados: OrdemEntregaSchema,
    db: AsyncSession = Depends(get_session)
):
    resultado = await db.execute(
        select(OrdemServicoModel).where(
            OrdemServicoModel.id == ordem_id
        )
    )

    ordem = resultado.scalar_one_or_none()

    if not ordem:
        raise HTTPException(
            status_code=404,
            detail='Ordem não encontrada.'
        )

    ordem.status = 'Entregue'
    ordem.data_saida = datetime.now()
    ordem.forma_pagamento = dados.forma_pagamento

    entrada = CaixaModel(
        tipo='entrada',
        descricao=f'Ordem de Serviço #{ordem.id}',
        valor=ordem.valor,
        forma_pagamento=dados.forma_pagamento
    )

    db.add(entrada)

    await db.commit()

    return {
        'mensagem': 'Ordem entregue e entrada registrada no caixa.',
        'ordem_id': ordem.id,
        'valor': ordem.valor,
        'forma_pagamento': dados.forma_pagamento
    }


@router.delete('/limpar-entregues-hoje')
async def limpar_ordens_entregues(
    db: AsyncSession = Depends(get_session)
):
    hoje = datetime.now().date()

    resultado = await db.execute(
        select(OrdemServicoModel).where(
            OrdemServicoModel.status.in_(['Entregue', 'entregue']),
            OrdemServicoModel.data_saida.is_not(None)
        )
    )

    ordens = resultado.scalars().all()
    quantidade = 0

    for ordem in ordens:
        data_saida = ordem.data_saida

        if hasattr(data_saida, 'date'):
            data_saida = data_saida.date()

        if data_saida < hoje:
            await db.delete(ordem)
            quantidade += 1

    await db.commit()

    return {
        'mensagem': 'Ordens antigas removidas.',
        'quantidade': quantidade
    }


@router.delete(
    '/{ordem_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def deletar_ordem_servico(
    ordem_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
    resultado = await db.execute(
        select(OrdemServicoModel).where(
            OrdemServicoModel.id == ordem_id
        )
    )

    ordem = resultado.scalar_one_or_none()

    if not ordem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ordem de serviço não encontrada.'
        )

    await db.delete(ordem)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)