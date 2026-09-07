from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.veiculo_model import VeiculoModel
from schemas.veiculo_schema import VeiculoSchema, VeiculoResponseSchema

from core.deps import get_session, get_current_user

router = APIRouter()

@router.post('/', response_model=VeiculoResponseSchema, status_code=status.HTTP_201_CREATED)
async def criar_veiculo(
    veiculo: VeiculoSchema,
    db: AsyncSession = Depends(get_session),
   
):
    
    novo_veiculo = VeiculoModel(**veiculo.model_dump())

    db.add(novo_veiculo)
    await db.commit()
    await db.refresh(novo_veiculo)

    return novo_veiculo

@router.get('/', response_model=List[VeiculoResponseSchema])
async def listar_veiculos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel)
        result = await session.execute(query)

        veiculos: List[VeiculoModel] = result.scalars().unique().all()

        return veiculos
    


@router.get('/{veiculo_id}', response_model=VeiculoResponseSchema, status_code=status.HTTP_200_OK)
async def obter_veiculo(veiculo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.id == veiculo_id)
        result = await session.execute(query)

        veiculo = result.scalars().unique().first()

        if not veiculo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Veículo não encontrado')
        else:
            return veiculo
        
    
@router.put('/{veiculo_id}', response_model=VeiculoResponseSchema, status_code=status.HTTP_200_OK)
async def atualizar_veiculo(
    veiculo_id: int, 
    veiculo_dados: VeiculoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
):

    async with db as session:
        query = select(VeiculoModel).filter(VeiculoModel.id == veiculo_id)
        result = await session.execute(query)
        veiculo_up = result.scalars().first()

        if not veiculo_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Veículo não encontrado')
    
        for chave, valor in veiculo_dados.model_dump().items():
            setattr(veiculo_up, chave, valor)

        await session.commit()
        await session.refresh(veiculo_up)
        return veiculo_up


@router.delete('/{veiculo_id}',status_code=status.HTTP_204_NO_CONTENT) 
async def deletar_veiculo(
    veiculo_id: int,
    db: AsyncSession = Depends(get_session), 
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
        
    
    query = select(VeiculoModel).filter(VeiculoModel.id == veiculo_id)
    result = await db.execute(query)
    veiculo = result.scalars().first()

    if not veiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Veículo não encontrado')

