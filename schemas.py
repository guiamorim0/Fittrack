from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerfilBase(BaseModel):
    peso: float
    altura: float
    objetivo: str

class PerfilCreate(PerfilBase):
    pass

class PerfilResponse(PerfilBase):
    id: int
    usuario_id: int
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    perfil: Optional[PerfilResponse] = None

    class Config:
        from_attributes = True

class TreinoBase(BaseModel):
    nome: str

class TreinoCreate(TreinoBase):
    pass

class TreinoResponse(TreinoBase):
    id: int
    usuario_id: int
    data: datetime
    class Config:
        from_attributes = True

class ExercicioBase(BaseModel):
    nome: str
    series: int
    repeticoes: int
    carga_kg: float

class ExercicioCreate(ExercicioBase):
    pass

class ExercicioResponse(ExercicioBase):
    id: int
    treino_id: int
    class Config:
        from_attributes = True

class TreinoComExercicios(TreinoResponse):
    exercicios: list[ExercicioResponse] = []

class UsuarioComTreinos(UsuarioResponse):
    treinos: list[TreinoResponse] = []

class Token(BaseModel):
    access_token: str
    token_type: str