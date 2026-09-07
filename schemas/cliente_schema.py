from pydantic import BaseModel 
from typing import Optional
from typing import List
from schemas.veiculo_schema import VeiculoResponseSchema

#O que o usuario envia para o banco de dados
class ClienteSchema(BaseModel):
    nome: str
    endereco: str | None= None
    telefone: str
    cpf: str | None = None
    
#Devolve para a tela sem cpf por privacidade
class ClienteResponseSchema(BaseModel):
    id: int
    nome: str
    endereco: str
    telefone: str

#aqui dizemos que o cliente tem uma lista de veiculos
    veiculos: list[VeiculoResponseSchema] = []
    
    class Config:
        from_attributes = True
