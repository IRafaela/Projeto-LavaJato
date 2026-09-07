from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.configs import settings

class FuncionarioModel(settings.DBBaseModel):
    __tablename__='funcionarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    endereco = Column(String(256), nullable=False)
    telefone = Column(String(20), nullable=False)
    salario = Column(Float, nullable=False)
    
    email = Column(String(256), unique=True, nullable=False)
    senha = Column(String(256), nullable=False)
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    
    criador = relationship(
        'UsuarioModel', back_populates='funcionarios',
         lazy='joined'
        
    )
    
    ordens_servico = relationship('OrdemServicoModel', back_populates='funcionario',
    cascade='all, delete-orphan'
    )