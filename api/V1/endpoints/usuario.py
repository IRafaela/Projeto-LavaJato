from typing import List, Optional, Any


from fastapi import APIRouter, status, Depends, HTTPException, Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha


router = APIRouter()

#GET LOGado
@router.get('/logado', response_model=UsuarioSchemaBase)
async def usuario_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


@router.post('/criar_usuario', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def criar_usuario(
    usuario: UsuarioSchemaCreate, 
    session: AsyncSession = Depends(get_session)
):
   novo_usuario = UsuarioModel(nome=usuario.nome, 
      sobrenome=usuario.sobrenome, 
      email=usuario.email, 
      senha=gerar_hash_senha(usuario.senha), 
      eh_admin=usuario.eh_admin
) 
   
   session.add(novo_usuario)
   await session.commit()
   await session.refresh(novo_usuario)

   return novo_usuario

#GET Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def listar_usuarios(
    db: AsyncSession = Depends(get_session),
    
):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()

        return usuarios


@router.get('/{usuario_id}', response_model=UsuarioSchemaBase,
status_code=status.HTTP_200_OK)
async def get_usuario(
    usuario_id: int, 
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.unique().scalars().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


#PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaUp,
status_code=status.HTTP_200_OK)
async def atualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioSchemaUp, 
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaUp = result.unique().scalars().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario_up.eh_admin is not None:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)

            await session.commit()

            return usuario_up
        
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


#DELETE Usuario        
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int, 
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.unique().scalars().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
    


