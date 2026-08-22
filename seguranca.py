import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") #a chave secreta que gera os tokens
ALGORITMO = "HS256" # algoritmo padrao pra JWT  
EXPIRACAO_MINUTOS = 60 #tempo que o vale antes de expirar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # a "ferramenta" do passlib que faz o hash com bcrypt

def gerar_hash(senha: str) -> str: #gera o hash da senha, recebe a senha e devolve o hash
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash: str) -> bool: # recebe a senha e aplica o hash na senha (nao tem como descriptografar)
    return pwd_context.verify(senha, hash)

def criar_token(dados: dict) -> str:
    para_codificar = dados.copy() # copia os dados que vao dentro do token ex: usuario_id
    expira = datetime.utcnow() + timedelta(minutes=EXPIRACAO_MINUTOS) # calcula quando o token expira, agora + 60 min
    para_codificar.update({"exp": expira}) # adiciona a validade do token
    token = jwt.encode(para_codificar, SECRET_KEY, algorithm=ALGORITMO) # cria o token assinado com a Secret key
    return token