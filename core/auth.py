from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/auth/'
)

async def autenticar_usuario(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = await db.execute(query)
    usuario: UsuarioModel = result.scalars().first()

    if not usuario:
        return None
    
    if not verificar_senha(senha, usuario.senha):
        return None
    
    return usuario
    
def _criar_token(tipo_token:str, tempo_vida: timedelta, sub: str) -> str:
  payload = {}
  sp = timezone('America/Sao_paulo') 
  expira = datetime.now(tz=sp) + tempo_vida

  payload['type'] = tipo_token

  payload['exp'] = int(expira.timestamp()) 

  payload['sub'] = str(sub)

  return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:

    return _criar_token(
        tipo_token='access_token', 
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub = sub
    
    )


