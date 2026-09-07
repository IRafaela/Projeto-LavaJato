from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    eh_admin: Optional[bool] = None



    class Config:
        from_attributes= True