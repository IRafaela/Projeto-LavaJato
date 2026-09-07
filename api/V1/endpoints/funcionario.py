from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.funcionario_model import FuncionarioModel
from schemas.funcionario_schema import FuncionarioCreateSchema,FuncionarioResponseSchema
from core.security import gerar_hash_senha
from core.deps import get_session, get_current_user


router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=FuncionarioResponseSchema)
async def criar_funcionario(
    funcionario: FuncionarioCreateSchema,
    db: AsyncSession = Depends(get_session),
    
):
    
    async with db as session:
        query = select(FuncionarioModel).filter(FuncionarioModel.email == funcionario.email)
        result = await session.execute(query)
        funcionario_existente = result.scalars().first()

        if funcionario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail='Já existe um funcionário cadastrado com este e-mail.'
            )
        
        dados_funcionario = funcionario.model_dump()
        dados_funcionario['senha'] = gerar_hash_senha(dados_funcionario['senha'])
   

        novo_funcionario = FuncionarioModel(**dados_funcionario)

    
        session.add(novo_funcionario)
        await session.commit()
        await session.refresh(novo_funcionario)

        return novo_funcionario
    

@router.get('/', response_model=List[FuncionarioResponseSchema],)
async def listar_funcionarios(db: AsyncSession = Depends(get_session)):
        query = select(FuncionarioModel)
        result = await db.execute(query)
        funcionarios = result.scalars().all()

        return funcionarios


@router.get('/{funcionario_id}', response_model=FuncionarioResponseSchema, status_code=status.HTTP_200_OK)
async def get_funcionario(funcionario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id)
        result = await db.execute(query)
        funcionario = result.scalars().unique().first()

        if not funcionario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Funcionário não encontrado')
        else:
            return funcionario

 #Rota para atualizar um cliente
@router.put('/{funcionario_id}', response_model=FuncionarioResponseSchema, status_code=status.HTTP_200_OK)
async def atualizar_funcionario(
    funcionario_id: int, 
    funcionario_dados: FuncionarioCreateSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
    

    async with db as session:
        query = select(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id)
        result = await session.execute(query)
        funcionario_up = result.scalars().first()

        if not funcionario_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Funcionário não encontrado')
    
        funcionario_up.nome = funcionario_dados.nome
        funcionario_up.endereco = funcionario_dados.endereco
        funcionario_up.telefone = funcionario_dados.telefone
        funcionario_up.salario = funcionario_dados.salario

        await session.commit()
        return funcionario_up  

@router.delete('/{funcionario_id}', status_code=status.HTTP_204_NO_CONTENT) 
async def deletar_funcionario(
    funcionario_id: int,
    db: AsyncSession = Depends(get_session), 
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
       
    
    query = select(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id)
    result = await db.execute(query)
    funcionario = result.scalars().first()

    if not funcionario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Funcionário não encontrado')
    
    await db.delete(funcionario)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
 