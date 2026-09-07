from fastapi import APIRouter

from api.V1.endpoints import cliente
from api.V1.endpoints import funcionario
from api.V1.endpoints import ordemservico
from api.V1.endpoints import usuario
from api.V1.endpoints import veiculo
from api.V1.endpoints import dashboard
from api.V1.endpoints import login
from api.V1.endpoints import caixa


api_router = APIRouter()

api_router.include_router(cliente.router, prefix='/clientes', tags=['Clientes'])
api_router.include_router(funcionario.router, prefix='/funcionarios', tags=['Funcionarios'])
api_router.include_router(ordemservico.router, prefix='/ordens-servico', tags=['Ordens de serviço'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['Usuarios'])
api_router.include_router(veiculo.router, prefix='/veiculos', tags=['Veiculos'])
api_router.include_router(dashboard.router, prefix='/dashboard', tags=['Dashboard'])
api_router.include_router(login.router, prefix='/auth', tags=['Login'])
api_router.include_router(caixa.router, prefix='/caixa', tags=['Caixa'])
