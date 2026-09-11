from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from schemas.veiculo_schema import VeiculoResponseSchema

#o que o usuario vai digitar no swagger
class OrdemServicoCreateSchema(BaseModel):
    tipo_lavagem: Optional[str] = None
    valor: Optional[float] = None
    status: Optional[str] = "Pendente"
    veiculo_id: Optional[int] = None
    funcionario_id: Optional[int] = None

#O que a api devolve como resposta.
class OrdemServicoResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo_lavagem: str
    valor: float
    data_entrada: datetime
    data_saida: Optional[datetime] = None
    veiculo_id: Optional[int] = None
    funcionario_id: Optional[int] = None

class OrdemEntregaSchema(BaseModel):
    forma_pagamento: str

    class Config:
        from_attributes= True