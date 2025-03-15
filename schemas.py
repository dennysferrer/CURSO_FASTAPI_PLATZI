from pydantic import BaseModel, field_validator, ValidationInfo
from pydantic.utils import GetterDict
from typing import Any
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_validator(cls, username, info: ValidationInfo):
        if len(username)<3 or len(username)>50:
            raise ValueError('la longitud del username debe ser mayor a 3 y menor de 50 caracteres')
        return username

    class ResponseModel(BaseModel):
        class Config:
            orm_mode = True
            getter_dict = PeeweeGetterDict

class userResponseModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    review: str
    score: int

    @field_validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El score debe estar entre 1 y 5')
        return score

class ReviewResponseModel(userResponseModel):
    id: int
    movie_id: int
    review: str
    score: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict




