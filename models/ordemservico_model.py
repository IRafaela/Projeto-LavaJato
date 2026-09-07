from sqlalchemy import Integer, String, Float, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings
from datetime import datetime


class OrdemServicoModel(settings.DBBaseModel):
      __tablename__='ordens_servico'

      id = Column(Integer, primary_key=True, autoincrement=True)
      tipo_lavagem = Column(String(50), nullable=True)
      valor = Column(Float, nullable=False)
      status = Column(String(30), default='Pendente')

      data_entrada = Column(DateTime, default=datetime.now)
      data_saida = Column(DateTime, nullable=True)

      veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=True)
      funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=True)

      veiculo = relationship('VeiculoModel', 
      back_populates='ordens_servico')
      funcionario = relationship('FuncionarioModel', back_populates='ordens_servico')
