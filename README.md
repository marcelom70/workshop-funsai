# API de Pessoas

Uma API simples para gerenciar informações de pessoas, construída com FastAPI e PostgreSQL.

## Requisitos

- Docker
- Docker Compose

## Como executar

1. Clone o repositório
2. Execute os containers:
```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

Acesse a documentação interativa em `http://localhost:8000/docs`

### Endpoints disponíveis:

- `POST /pessoas/`: Criar uma nova pessoa
- `GET /pessoas/`: Listar todas as pessoas
- `GET /pessoas/{id}`: Buscar uma pessoa específica
- `PUT /pessoas/{id}`: Atualizar uma pessoa
- `DELETE /pessoas/{id}`: Deletar uma pessoa

## Exemplo de payload para criar/atualizar uma pessoa:

```json
{
    "nome": "João Silva",
    "profissao": "Desenvolvedor",
    "idade": 30,
    "hobby": "Leitura"
}
``` 