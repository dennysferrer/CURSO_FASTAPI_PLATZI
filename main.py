from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, UserReview
from schemas import UserRequestModel, userResponseModel, ReviewRequestModel, ReviewResponseModel
from typing import List


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


@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews():
    return UserReview.select()



@app.post('/user', response_model=userResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        return HTTPException(status_code=409, detail='El usuario ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_password
    )

    user = userResponseModel(
        id=user.id,
        username=user.username
    )
    return user


@app.post('/reviews', response_model=ReviewRequestModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user).firts() is None:
        return HTTPException(status_code=404, detail='El usuario no existe')

    if Movie.select().where(Movie.id == user_review.movie).firts() is None:
        return HTTPException(status_code=404, detail='La película no existe')

    user_review = UserReview.create(
        user_id=user_review.user,
        movie_id=user_review.movie,
        review=user_review.review,
        score=user_review.score
    )

    return user_review