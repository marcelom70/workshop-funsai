from typing import Optional, Dict, Any
import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from . import models, config
import httpx

# Schema para function calling
get_person_info_schema = {
    "type": "function",
    "function": {
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
                    "enum": ["profissao", "idade", "hobby"],
                    "description": "Tipo de informação solicitada"
                }
            },
            "required": ["nome"]
        }
    }
}

def get_person_info(db: Session, nome: str, info_requerida: Optional[str] = None) -> Dict[str, Any]:
    """Busca informações de uma pessoa no banco de dados."""
    query = db.query(models.Pessoa).filter(models.Pessoa.nome.ilike(f"%{nome}%"))
    pessoa = query.first()
    
    if not pessoa:
        return {"error": f"Pessoa com nome '{nome}' não encontrada"}
    
    if info_requerida:
        if hasattr(pessoa, info_requerida):
            return {info_requerida: getattr(pessoa, info_requerida)}
        else:
            return {"error": f"Informação '{info_requerida}' não disponível"}
    
    return {
        "nome": pessoa.nome,
        "profissao": pessoa.profissao,
        "idade": pessoa.idade,
        "hobby": pessoa.hobby
    }

def process_chat_query(db: Session, user_query: str) -> str:
    """Processa a pergunta do usuário usando OpenAI e banco de dados."""
    try:
        # Configuração do cliente OpenAI com httpx
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            http_client=httpx.Client(),
        )

        # Primeira chamada para OpenAI para interpretar a pergunta
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda a buscar informações sobre pessoas no banco de dados."},
                {"role": "user", "content": user_query}
            ],
            tools=[get_person_info_schema],
            tool_choice="auto"
        )

        # Se não houver uma chamada de função, retorna a resposta direta
        if not response.choices[0].message.tool_calls:
            return "Desculpe, não entendi sua pergunta. Pode reformular?"

        # Extrai os parâmetros da chamada de função
        tool_call = response.choices[0].message.tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)
        
        # Busca as informações no banco de dados
        db_response = get_person_info(
            db=db,
            nome=function_args.get("nome"),
            info_requerida=function_args.get("info_requerida")
        )

        # Se houver erro na busca, retorna a mensagem de erro
        if "error" in db_response:
            return db_response["error"]

        # Segunda chamada para OpenAI para formatar a resposta
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda a buscar informações sobre pessoas no banco de dados."},
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": None, "tool_calls": [tool_call]},
                {"role": "tool", "content": str(db_response), "tool_call_id": tool_call.id}
            ]
        )

        return final_response.choices[0].message.content

    except Exception as e:
        return f"Erro ao processar sua pergunta: {str(e)}" 