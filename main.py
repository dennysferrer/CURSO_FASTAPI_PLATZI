from fastapi import FastAPI
from database import database as connection
from database import User, Movie, UserReview
from schemas import UserBaseModel


app = FastAPI(
    title='App',
    description='App de estudio de fastapi',
    version='0.0.1'
)


@app.on_event('startup')
async def start_up():
    print('Iniciando app...')
    if connection.is_closed():
        connection.connect()
        print('Conexión establecida...')
    connection.create_tables([User, Movie, UserReview])



@app.on_event('shutdown')
async def shut_down():
    print('Cerrando app...')
    if not connection.is_closed():
        connection.close()
        print('Conexión cerrada...')


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.post('/user')
async def create_user(user: UserBaseModel):
    user = User.create(
        username=user.username,
        password=user.password
    )

    return user.id