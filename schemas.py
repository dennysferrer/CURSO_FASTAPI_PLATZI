from pydantic import BaseModel, field_validator, ValidationInfo

class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_validator(cls, username, info: ValidationInfo):
        if len(username)<3 or len(username)>50:
            raise ValueError('la longitud del username debe ser mayor a 3 y menor de 50 caracteres')
        return username

class userResponseModel(BaseModel):
    id: int
    username: str



