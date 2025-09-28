#Comando para rodar o venv
#.venv\Scripts\activate.bat

#Comando para rodar o servidor (uviorn)
#uvicorn main:app --reload


#Comando para criar ou atualizar o banco de dados

#gerar o arquivo de migração
#alembic revision --autogenerate -m "create users and orders tables"
#alembic upgrade head

# USUARIO TESTE
# USUARIO: senha123456@teste.com
# SENHA:   senha123456@teste.com

from fastapi import FastAPI 
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
#import uvicorn
import os

# exemplo de env

#SECRET_KEY = %yemi5q-3*ksjgm1=t&$#t^1eq2t6q+vr@zs8v7=sw+01i@v(u
#ALGORITHM = HS256
#ACCESS_TOKEN_EXPIRE_MINUTES = 60
#REFRESH_TOKEN_EXPIRE_DAYS = 7

load_dotenv()

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# if __name__ == "__main__":
#     uvicorn.run(app, port=8000)