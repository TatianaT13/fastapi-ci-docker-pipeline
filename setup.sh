#!/usr/bin/env bash
set -e

mkdir -p logs
rm -f logs/api_test.log log.txt

docker image pull datascientest/fastapi:1.0.0

docker compose up --build --abort-on-container-exit --exit-code-from test_content | tee log.txt

echo "Logs agrégés: logs/api_test.log"
echo "Sortie console: log.txt"
