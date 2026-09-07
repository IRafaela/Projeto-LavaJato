from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String

from core.configs import settings

class CaixaModel(settings.DBBaseModel):
    __tablename__ = 'caixa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(30), nullable=False)
    descricao = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    forma_pagamento = Column(String(50), nullable=True)
    data_hora = Column(DateTime, default=datetime.now)
    

