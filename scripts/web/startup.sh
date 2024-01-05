#!/usr/bin/env bash

echo "Start service"

python scripts/migrate.py

exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT