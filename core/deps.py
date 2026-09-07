from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.configs import settings
from core.auth import oauth2_schema
from models.usuario_model import UsuarioModel

class Tokendata(BaseModel):
    username: Optional[str] = None


async def get_session() -> AsyncGenerator:
    db: AsyncSession = Session()
    try:
       yield db
    finally:
        await db.close()

async def get_current_user(
  db: AsyncSession = Depends(get_session),
  token: str = Depends(oauth2_schema)    
) -> UsuarioModel:
    
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Não foi possível validar a credencial', headers={'www-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM],
            options={'verify_aud': False}
        )
        
        username: str = payload.get('sub')
        

        if username is None:
            raise credential_exception
        
        token_data = Tokendata(username=username)
    
    except JWTError as e:
        raise credential_exception
    
    
    async with db as session:
       query = select(UsuarioModel).filter(UsuarioModel.id == int(username))
       result = await db.execute(query)
       usuario: UsuarioModel = result.scalars().unique().one_or_none()
        
    if usuario is None:
        raise credential_exception
    
    return usuario

