from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import base

class Usuario(base):
    __tablename__ = 'usuarios'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    nome = Column(String)
    email = Column(
        String,
        unique=True
    )
    senha_hash = Column(String)

    perfil = relationship(
        "PerfilFitness", back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
        )

    treinos = relationship(
        "Treino", back_populates="usuario",
        cascade="all, delete-orphan"
        )

class PerfilFitness(base):
    __tablename__ = 'perfis'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    usuario_id = Column(
        Integer,
        ForeignKey('usuarios.id'),
        unique=True
    )
    peso = Column(Float)
    altura = Column(Float)
    objetivo = Column(String)

    usuario = relationship("Usuario", back_populates="perfil")

class Treino(base):
    __tablename__ = 'treinos'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    usuario_id = Column(
        Integer,
        ForeignKey('usuarios.id')
    )
    nome = Column(String)
    data = Column(DateTime)

    usuario = relationship("Usuario", back_populates="treinos")
    exercicios = relationship("Exercicio", back_populates="treino", cascade="all, delete-orphan")

class Exercicio(base):
    __tablename__ = 'exercicios'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    treino_id = Column(
        Integer,
        ForeignKey('treinos.id')
    )
    nome = Column(String)
    series = Column(Integer)
    repeticoes = Column(Integer)
    carga_kg = Column(Float)

    treino = relationship("Treino", back_populates="exercicios")