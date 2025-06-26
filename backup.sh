#!/bin/bash

# Criar backup
docker exec -i workshop-funsai-db-1 pg_dump -U user -d pessoas_db > dump.sql

# Para restaurar o backup, use:
# docker exec -i workshop-funsai-db-1 psql -U user -d pessoas_db < dump.sql 