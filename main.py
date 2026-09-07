from fastapi import FastAPI

from core.configs import settings
from api.V1.api import api_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title='Sistema de Gerenciamento de Lava Jato', version='1.0')
app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount('/static', StaticFiles(directory='frontend/static'), name='static')




@app.get('/veiculos')
async def abrir_tela_veiculos():
    return FileResponse('frontend/veiculos.html')

@app.get('/clientes')
async def abrir_clientes():
    return FileResponse('frontend/clientes.html')


@app.get('/funcionarios')
async def abrir_funcionarios():
    return FileResponse('frontend/funcionarios.html')


@app.get('/ordens-servico')
async def abrir_ordens():
    return FileResponse('frontend/ordemservico.html')


@app.get('/usuarios')
async def abrir_usuarios():
    return FileResponse('frontend/usuarios.html')

@app.get('/dashboard')
async def retornar_tela_dashboard():
    return FileResponse('frontend/dashboard.html')

@app.get('/auth')
async def abrir_login():
    return FileResponse('frontend/login.html')

@app.get('/caixa')
async def retornar_tela_caixa():
    return FileResponse('frontend/caixa.html')





if __name__=='__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)