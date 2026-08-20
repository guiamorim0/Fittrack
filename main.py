from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
import models
import schemas
from database import engine, session_local
from datetime import datetime

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


@app.post(
    '/usuarios/{usuario_id}/perfil',
    response_model= schemas.PerfilResponse)
def criar_perfil(usuario_id: int, perfil: schemas.PerfilCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")

    if usuario.perfil:
        raise HTTPException(status_code=400, detail="Usuario ja possui perfil!")

    db_perfil = models.PerfilFitness(
        usuario_id=usuario_id,
        peso=perfil.peso,
        altura=perfil.altura,
        objetivo=perfil.objetivo
    )
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

@app.get(
    '/usuarios/{usuario_id}/perfil',
    response_model= schemas.PerfilResponse)
def buscar_perfil(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
    if not usuario.perfil:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado!")
    return usuario.perfil

@app.post(
    '/usuarios/{usuario_id}/treinos',
    response_model= schemas.TreinoResponse)
def criar_treino(usuario_id: int, treino: schemas.TreinoCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")

    db_treino = models.Treino(
        usuario_id=usuario_id,
        nome=treino.nome,
        data=datetime.now()
    )
    db.add(db_treino)
    db.commit()
    db.refresh(db_treino)
    return db_treino

@app.get(
    '/treinos/{treino_id}',
    response_model= schemas.TreinoResponse)
def ler_treino(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino nao encontrado!")
    return treino

@app.delete(
    '/treinos/{treino_id}')
def remover_treino(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino nao encontrado!")
    db.delete(treino)
    db.commit()
    return {"mensagem": "Treino removido com sucesso!"}

@app.post(
    '/treinos/{treino_id}/exercicios',
    response_model= schemas.ExercicioResponse)
def criar_exercicio(treino_id: int, exercicio: schemas.ExercicioCreate, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino nao encontrado!")

    db_exercicio = models.Exercicio(
        treino_id = treino_id,
        nome=exercicio.nome,
        series=exercicio.series,
        repeticoes=exercicio.repeticoes,
        carga_kg=exercicio.carga_kg
    )
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

@app.get(
    '/treinos/{treino_id}/exercicios',
    response_model= List[schemas.ExercicioResponse])
def listar_exercicios(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino nao encontrado!")
    return treino.exercicios

@app.delete(
    '/exercicios/{exercicio_id}')
def remover_exercicio(exercicio_id: int, db: Session = Depends(get_db)):
    exercicio = db.query(models.Exercicio).filter(models.Exercicio.id == exercicio_id).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado!")
    db.delete(exercicio)
    db.commit()
    return {"mensagem": "Exercicio removido com sucesso!"}

@app.get(
    '/treinos/{treino_id}/completo',
    response_model= schemas.TreinoComExercicios)
def treino_completo(treino_id: int, db: Session = Depends(get_db)):
    treino = db.query(models.Treino).options(joinedload(models.Treino.exercicios)).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino nao encontrado!")
    return treino

@app.get(
    '/usuarios/{usuario_id}/treinos',
    response_model= schemas.UsuarioComTreinos)
def usuario_com_treinos(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).options(joinedload(models.Usuario.treinos)).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado!")
    return usuario

