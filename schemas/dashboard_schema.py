from pydantic import BaseModel

class DashboardResponse(BaseModel):
    clientes: int
    veiculos: int
    ordensServico: int


    class Config:
        from_attributes = True