from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from . import models, schemas, chat_service
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Pessoas")

@app.post("/pessoas/", response_model=schemas.Pessoa)
def create_pessoa(pessoa: schemas.PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = models.Pessoa(**pessoa.model_dump())
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@app.get("/pessoas/", response_model=List[schemas.Pessoa])
def read_pessoas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pessoas = db.query(models.Pessoa).offset(skip).limit(limit).all()
    return pessoas

@app.get("/pessoas/{pessoa_id}", response_model=schemas.Pessoa)
def read_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    db_pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return db_pessoa

@app.put("/pessoas/{pessoa_id}", response_model=schemas.Pessoa)
def update_pessoa(pessoa_id: int, pessoa: schemas.PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    
    for key, value in pessoa.model_dump().items():
        setattr(db_pessoa, key, value)
    
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@app.delete("/pessoas/{pessoa_id}")
def delete_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    db_pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if db_pessoa is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    
    db.delete(db_pessoa)
    db.commit()
    return {"message": "Pessoa deletada com sucesso"}

class ChatQuery(BaseModel):
    query: str

@app.post("/chat/", response_model=dict)
def chat_with_database(chat_query: ChatQuery, db: Session = Depends(get_db)):
    """
    Endpoint para fazer perguntas em linguagem natural sobre as pessoas no banco de dados.
    A resposta será processada pela OpenAI para fornecer uma resposta natural.
    """
    try:
        response = chat_service.process_chat_query(db, chat_query.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 