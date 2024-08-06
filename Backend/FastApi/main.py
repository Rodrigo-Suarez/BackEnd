### FastAPI ###

from fastapi import FastAPI
from routers import products, users, user_auth_jwt, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ROUTERS
app.include_router(products.router)
app.include_router(users.router)
app.include_router(user_auth_jwt.router)
app.include_router(users_db.router)

# RECURSOS ESTÁTICOS
app.mount("/static", StaticFiles(directory= "static"), name="static")

@app.get("/")

async def root():
    return "LCDTM"


@app.get("/url")

async def url():
    return {"url":"messi.com"}