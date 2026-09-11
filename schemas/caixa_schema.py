from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_hora: datetime


     
