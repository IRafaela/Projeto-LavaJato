from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.security import gerar_hash_senha
from core.auth import criar_token_acesso
from core.auth import autenticar_usuario

from models.usuario_model import UsuarioModel

router = APIRouter()



@router.post('/')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_session)
    ):
    usuario = await autenticar_usuario(form_data.username, form_data.password, db=session)
  
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
        
   
    return JSONResponse(content={'access_token': criar_token_acesso(sub=usuario.id), 'token_type': 'bearer'})

@router.put('/recuperar-senha')
async def recuperar_senha(request: Request, db: AsyncSession = Depends(get_session)):
    dados = await request.json()

    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    if not email or not nova_senha:
        raise HTTPException(status_code=422, detail='E-mail e senha sao obrigatórios.')

    query = select(UsuarioModel).where(UsuarioModel.email == email)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado.')

    usuario.senha = gerar_hash_senha(nova_senha)

    await db.commit()
    
   
    return {'message': 'Senha atualizada com sucesso!'}
