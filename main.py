from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, session_local

models.base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post(
    '/usuarios/',
    response_model= schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate ,db: Session = Depends(get_db)):
    existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email ja cadastrado!")

    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get(
    '/usuarios/',
    response_model= List[schemas.UsuarioResponse])
def read_usuarios(db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).all()
    return usuario

@app.get(
    '/usuarios/{usuario_id}',
    response_model= schemas.UsuarioResponse)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
    return usuario

@app.delete(
    '/usuarios/{usuario_id}')
def remover_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
    db.delete(db_usuario)
    db.commit()
    return {"mensagem": "Usuario removido com sucesso!"}
