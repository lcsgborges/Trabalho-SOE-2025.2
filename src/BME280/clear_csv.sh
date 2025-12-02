#!/bin/bash

# Script para limpar apenas o arquivo CSV de dados

echo "=== Limpeza do CSV ==="

CSV_PATH="../database/data.csv"

if [ -f "$CSV_PATH" ]; then
    echo "Removendo arquivo CSV..."
    rm -f "$CSV_PATH"
    echo "CSV removido com sucesso!"
else
    echo "CSV não encontrado em $CSV_PATH"
fi

echo ""
echo "O CSV será recriado automaticamente quando o servidor"
echo "fizer a próxima leitura do sensor."
