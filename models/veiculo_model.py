from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings

class VeiculoModel(settings.DBBaseModel):
    __tablename__='veiculos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String(8), unique=True, nullable=False, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=True)
    cor = Column(String(30), nullable=True)
    tipo = Column(String(30), nullable=True)

    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    dono = relationship('ClienteModel', 
    back_populates='veiculos')
    
    ordens_servico = relationship('OrdemServicoModel', 
    back_populates='veiculo')
    
