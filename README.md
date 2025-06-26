Bom, pessoal, na hora do workshop as coisas não deram muito certo, não é mesmo???

Pois é, voltei pra casa e, usando o mesmo projeto e o mesmo modelo de IA (claude 3.5 sonnet) ainda dentro do Cursor.ai e adivinha? FUNCIONOU!

Bastava só insistir mais um pouco que ele resolvia, mas não tivemos tempo suficiente durante o workshop... snif

O código todo está aqui e sintam-se à vontade em usá-lo e reproduzir tudo o que foi feito.


Apenas, como resumo as atividades que fizemos, aqui vai o roteiro que utilizei durante a atividade: 

Pré-requisitos de ambiente:

    Docker.io e docker-compose instalados.
    
    Python, versão 3.11.9
    
    Cursor.ai

Atividades para preparação do ambiente:

    - montar um servidor na scaleway, atualizar, instalar docker e docker-compose.
    
    - excluir knownhost da máquina local.
    
    - excluir imagens e tags da máquina local.
    
    - excluir containers, redes e volumes da máquina local.
    
    - garantir que o postgres local não esteja rodando: sudo systemctl status postgresql
    
    - criação de diretório chamado workshop-funsai
    
    - cópia do diretório .cursor para dentro desse diretório.
    
    - criação de um environment python nesse diretório.
    
    - criação de um arquivo .env e inclusão da chave openai.
    
    - Como segurança, se achar prudente, rodar a criação da variável de ambiente OPENAI_API_KEY no terminal principal (nesse caso, já deve estar aberto).
    
    - Preparar playlist com músicas feitas com IA.
    
    - Deixar uma instância do browser com abas selecionadas para serem exibidas (Cursor, bit.ly, Scaleway, dockerhub, openai, deepseek, klingai, lovable, docker e outra     com abas úteis a serem ocultadas (roteiro azure, email, etc).


Passos para implementação do programa:

    - Abrir o cursor.ai no diretório workshop-funsai
    
    - inclusão do contexto de .cursor
    
    - submeter o primeiro prompt: "Eu quero uma aplicação que possua uma API que acesse uma base de dados Postgres e que tenha uma tabela simples, chamada Pessoa, com os atributos Id, Nome, Profissão, idade e hobby. Tanto a aplicação quanto o banco de dados devem rodar dentro de containers."
    
    - Submeter o segundo prompt: "Quero um método na API para um chat que integra OpenAI API com um banco de dados local. Aqui estão os requisitos técnicos:
    


  1. **Estrutura do Banco de Dados**:
     - Tabela `pessoas` com campos já existentes na tabela

  2. **Funcionalidade Principal**:
     - Receber perguntas naturais do usuário (ex: "Qual a profissão de João da Silva?")
     - Converter para chamada de API OpenAI com function calling
     - Executar query no banco local
     - Formatar resposta natural

  3. **Esquema da Função (Function Calling)**:
  ```python
  get_person_info_schema = {
  	"name": "get_person_info",
  	"description": "Busca informações de pessoas no banco de dados local",
  	"parameters": {
  		"type": "object",
  		"properties": {
  			"nome": {
  				"type": "string",
  				"description": "Nome completo da pessoa"
  			},
  			"info_requerida": {
  				"type": "string",
  				"enum": ["profissao", etc...],
  				"description": "Tipo de informação solicitada"
  			}
  		},
  		"required": ["nome"]
  	}
  }
  Fluxo Completo:

  Usuário pergunta: "Qual a profissão de João da Silva?"

  Sistema envia para OpenAI com o schema

  OpenAI devolve chamada para get_person_info

  Seu código executa a query SQL:

  sql
  SELECT profissao FROM pessoas WHERE nome = 'João da Silva';
  Sistema envia resposta bruta de volta para OpenAI

  OpenAI formata: "João da Silva é vendedor"

  Requisitos Técnicos:

  Use Python com FastAPI ou Flask para o backend

  Biblioteca openai v1.0+

  Tratamento de erros robusto"

Começar com os testes usando openai.

    - verificar possíveis erros. Atentar para a chave e o uso do arquivo .env.

    - submeter terceiro prompt: "Quero que criei uma interface web que acesse o método de chat, para ficar mais amigável para o usuário."

Passos preparatório para subir na nuvem (máquina local):

    - Criar tag da imagem web, com o prefixo na docker.hub

    - Fazer push da imagem web

    - Fazer cópia do conteúdo do arquivo, usando o comando: docker exec -t [nome do container do postgres] pg_dump -U user -d pessoas_db > dump.sql

    - Criar cópia do docker-compose.yaml, removendo o volume do web e alterando para a imagem

    - Fazer scp dos arquivos dump.sql e docker-compose.yaml com o comando docker exec -i [nome-do-container] psql -U postgres -d [nome do banco] < dump.sql

Passos preparatório para subir na nuvem (máquina nuvem):

    - executar docker-compose com o arquivo

    - verificar se está tudo rodando.

    - executar restore dos dados no container do postgres, com o comando: docker exec -i [nome-do-container] psql -U postgres -d [nome do banco] < dump.sql.

    - fazer um teste básico do funcionamento.


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
