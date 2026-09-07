from pydantic import BaseModel 
from typing import Optional

from datetime import datetime

class CaixaSchemaBase(BaseModel):
    tipo: str
    descricao: str
    valor: float
    forma_pagamento: Optional[str] = None

class CaixaSchemaCreate(CaixaSchemaBase):
    tipo: str
    descricao: str
    valor: float
    forma_pagamento: Optional[str] = None

class CaixaSchema(CaixaSchemaBase):
    id: int
    data_hora: datetime


    class config:
        from_attributes = True


     
