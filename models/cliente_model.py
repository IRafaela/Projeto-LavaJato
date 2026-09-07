from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class ClienteModel(settings.DBBaseModel):
    __tablename__='clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(256), nullable=False)
    telefone = Column(String(20), nullable=False)
    cpf = Column(String(14), unique=True, nullable=True)


    veiculos = relationship(
        'VeiculoModel', 
         back_populates='dono',
         cascade='all, delete-orphan'
    )


    