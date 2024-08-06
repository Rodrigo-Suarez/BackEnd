from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"], responses={404 : {"error":"No encontrado"}})

class User(BaseModel):
    id: int
    name: str
    

prod_list = [User(id=1, name="producto 1"),
             User(id=2, name="producto 2"),
             User(id=3, name="producto 3"),
             User(id=4, name="producto 4"),
             User(id=5, name="producto 5")]


@router.get("/")
async def product():
    return prod_list

@router.get("/{id}")
async def product(id: int):
    return await search_prod(id)




async def search_prod(id: int):
    users = filter(lambda product: product.id == id, prod_list)
    try:
        return list(users)[0]
    except:
        return {"error":"El producto con la ID mencionada no existe"}