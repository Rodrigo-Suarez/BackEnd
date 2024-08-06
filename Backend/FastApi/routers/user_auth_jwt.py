from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

#Tipo de algoritmo
Algorithm = "HS256"
token_duration = 1
secret = "83a8b9fc8b0f76f9d81e6be1b4f92a9a33c0e32d7f9b1e9e35a4a3f55b1cdae8"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

#Algoritmo de encriptación
crypto = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


user_list = {
    "Choi":{
        "username" : "Choi",
        "fullname" : "Rodrigo Suarez",
        "email" : "Rodrigo@gmail.com",
        "disabled" : False,
        "password" : "$2a$12$n/IqU/RjqkKeLrVa2xKtl.Tj3UulaCudL5cVPBSJ8RdUfHTOwxCPi"
    },

    "Choi2":{
        "username" : "Choi2",
        "fullname" : "Rodrigo Suarez",
        "email" : "Rodrigo2@gmail.com",
        "disabled" : True,
        "password" : "$2a$12$CU52awoH0bz6ylg0SqrP/e2kj0Y8hUGSPKUWwYbAaDMar6dqRCxvS"
    }
}


def search_user_db(username: str):
    if username in user_list:
        return UserDB(**user_list[username])
    
    return "no se encontro el usuario"


def search_user(username: str):
    if username in user_list:
        return User(**user_list[username])
    
    return "no se encontro el usuario"


def decrypt(token: str = Depends(oauth2)):
    decrypt_token = jwt.decode(token, secret, algorithms= Algorithm).get("sub")
    user = search_user(decrypt_token)

    if user is None:
        raise HTTPException(status_code= 401)
    
    return user


def current_user(user: User = Depends(decrypt)):
    
    if user.disabled:
        raise HTTPException(status_code= 401, detail="Usuario inactivo")
    
    return user




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = user_list.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    
    if not crypto.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes= token_duration)
    }

    return {"access_token":  jwt.encode(access_token, secret, algorithm= Algorithm) , "token_type": "bearer"}



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
