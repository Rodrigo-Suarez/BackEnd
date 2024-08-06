from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

#Variable que guarda el valor del token
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password" : "12345"
    },

    "Choi2":{
        "username" : "Choi2",
        "fullname" : "Rodrigo Suarez",
        "email" : "Rodrigo2@gmail.com",
        "disabled" : True,
        "password" : "54321"
    }
}


# Funcion que busca si un usuario existe como usuario de base de datos(es decir, icluye contraseña)
def search_user_db(username: str):
    if username in user_list:
        return UserDB(**user_list[username])
    
    return "no se encontro el usuario"

# Funcion que busca si un usuario existe(sin incluir contraseña) 
def search_user(username: str):
    if username in user_list:
        return User(**user_list[username])
    
    return "no se encontro el usuario"

#Utiliza el token para verificar el usuario
def current_user(token: str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(status_code= 401)
    
    if user.disabled:
        raise HTTPException(status_code= 401, detail="Usuario inactivo")
    
    return user


#Formulario de autentificacion de usuario (nombre y contraseña)
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = user_list.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return {"access_token": user.username , "token_type": "bearer"}


#Retorna los datos del usuario cuando ya esta autenticado
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user