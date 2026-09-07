from pydantic import BaseModel
from typing import Optional

class VeiculoSchema(BaseModel):
    placa: str
    marca: str
    modelo: Optional[str] = None
    cor: Optional[str] = None
    
    cliente_id: int

class VeiculoResponseSchema(VeiculoSchema):
    id: int

    class Config:
        from_attributes = True

