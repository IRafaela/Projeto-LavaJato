from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.cliente_model import ClienteModel
from models.veiculo_model import VeiculoModel
from models.funcionario_model import FuncionarioModel
from models.ordemservico_model import OrdemServicoModel

from core.database import get_session


router = APIRouter()


@router.get("/")
async def get_dashboard(db: AsyncSession = Depends(get_session)):
  
  total_clientes = await db.scalar(
      select(func.count()).select_from(ClienteModel)
  )
  total_veiculos = await db.scalar(
      select(func.count()).select_from(VeiculoModel)
  )
  total_funcionarios = await db.scalar(
      select(func.count()).select_from(FuncionarioModel)
  )
  total_ordens = await db.scalar(
      select(func.count()).select_from(OrdemServicoModel)
      .filter(OrdemServicoModel.status != 'Entregue')
  ) or 0

  result = await db.execute(
    select(OrdemServicoModel).filter(OrdemServicoModel.status != 'Entregue')
  )
  ordens_pendentes = result.scalars().all()

  return {
      'clientes': total_clientes or 0,
      'veiculos': total_veiculos or 0,
      'funcionarios': total_funcionarios or 0,
      'ordensServico': total_ordens,
      'ordensPendentes': ordens_pendentes
  }