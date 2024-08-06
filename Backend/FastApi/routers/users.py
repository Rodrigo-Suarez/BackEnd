from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [User(id = 1, name = "Rodrigo", surname = "Suarez", age = 17),
              User(id = 2, name = "Pedro", surname = "Gonzalez", age = 71),
              User(id = 3, name = "Juan", surname = "Martinez", age = 37)]




# //*GET*\\

@router.get("/users")
async def users():
    return users_list


# PATH
@router.get("/user/{id}")
async def user(id: int):
    return await search_user(id)


# QUERY

@router.get("/user_query/")
async def user(id: int):
    return await search_user(id)



# //*POST*\\

@router.post("/user/", status_code=201, response_model=User)
async def user(user: User):
    for user_id in users_list:
        if user_id.id == user.id:
            raise HTTPException(status_code=404, detail="El usuario ya existe")
        
    users_list.append(user)
    return user



# //*PUT*\\

@router.put("/user/")
async def user(user: User):

    found = False

    for index, user_in_list in enumerate(users_list):
        if user_in_list.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"El usuario con la ID mencionada no existe"}
    
    return user



# //*DELETE*\\

@router.delete("/user/{id}")
async def user(id: int):
    
    found = False

    for index, user_in_list in enumerate(users_list):
        if user_in_list.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"error": "No se elimino el usuario"}
    




async def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"El usuario con la ID mencionada no existe"}