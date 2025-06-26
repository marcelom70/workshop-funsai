#!/bin/bash

# Nome do container do banco de dados
DB_CONTAINER="root_db_1"

# Configurações do banco de dados
DB_NAME="pessoas_db"
DB_USER="user"

# Verifica se o container está rodando
if ! docker ps | grep -q $DB_CONTAINER; then
    echo "Erro: Container $DB_CONTAINER não está rodando"
    exit 1
fi

# Verifica se o arquivo dump existe
if [ ! -f dump.sql ]; then
    echo "Erro: Arquivo dump.sql não encontrado"
    exit 1
fi

# Verifica se o banco de dados existe, se não, cria
docker exec -i $DB_CONTAINER psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME
if [ $? -ne 0 ]; then
    echo "Criando banco de dados $DB_NAME..."
    docker exec -i $DB_CONTAINER createdb -U $DB_USER $DB_NAME
fi

# Limpa o banco de dados existente (opcional, remova se quiser preservar dados existentes)
echo "Limpando banco de dados existente..."
docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restaura o dump
echo "Restaurando dump..."
cat dump.sql | docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME

if [ $? -eq 0 ]; then
    echo "Restauração concluída com sucesso!"
else
    echo "Erro durante a restauração"
    exit 1
fi 