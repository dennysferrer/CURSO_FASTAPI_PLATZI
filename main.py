from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, UserReview
from schemas import UserRequestModel, userResponseModel


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


@app.post('/user', response_model=userResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail='El usuario ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_password
    )

    return userResponseModel(
        id=user.id,
        username=user.username
    )