from pydantic import BaseModel

class PessoaBase(BaseModel):
    nome: str
    profissao: str
    idade: int
    hobby: str | None = None

class PessoaCreate(PessoaBase):
    pass

class Pessoa(PessoaBase):
    id: int

    class Config:
        from_attributes = True 