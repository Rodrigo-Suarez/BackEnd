from fastapi import APIRouter, HTTPException
from db.models.users import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/usersdb", tags=["usersdb"])


# //*GET*\\

@router.get("/")
async def users():
    return users_schema(db_client.users.find())


# PATH
@router.get("/{id}")
async def user(id: str):
    return await search_user("_id", ObjectId(id))


# QUERY

@router.get("/user_query/")
async def user(id: str):
    return await search_user("_id", ObjectId(id))



# //*POST*\\

@router.post("/", status_code=201, response_model=User)
async def user(user: User):
    email = db_client.users.find_one({"email":user.email})
    if email:
            raise HTTPException(status_code=404, detail="El usuario ya existe")
        
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)



# //*PUT*\\

@router.put("/", response_model= User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    
    except:
        return {"error": "No se ha actualizado el usuario"}

    return await search_user("_id", ObjectId(user.id))



# //*DELETE*\\

@router.delete("/{id}")
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    
    if not found:
        return {"error": "No se elimino el usuario"}
    



#async def search_user_by_email(email: str):
#    user = db_client.local.users.find_one({"email": email})
#    try:
#        return user
#    except:
#        return {"error":"El usuario con la ID mencionada no existe"}


async def search_user(field: str, key):
    user = db_client.users.find_one({field:key})
    try:
        return User(**user_schema(user))
    except:
        return {"error":"El usuario con la ID mencionada no existe"}


