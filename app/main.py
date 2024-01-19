from fastapi import FastAPI
from plan.routers import ipr_router, task_router


"""
Как сделать версионирование
def create_app():
    app = FastAPI()

    app.include_router(book_routers_v1.router, prefix="/v1")

    return app
"""

app = FastAPI()

app.include_router(ipr_router)
app.include_router(task_router)


app = FastAPI()  # lifespan


@app.get('/ping')
async def ping():
    """Проверка работы сервера"""
    return {'app': 'Hackathon Alfa Task App v1.0'}


@app.get('/employee')
async def get_employee():
    """Поиск группы или определенного сотрудника
    по id, fullName, subdivision, position"""
    pass
