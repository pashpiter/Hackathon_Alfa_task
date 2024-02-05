#!/bin/bash

set -e

while ! nc -z $SERVER_HOST $SERVER_PORT; do
  echo "Waiting for FastAPI to start..."
  sleep 1
done
echo "FastAPI started"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for Postgres to start..."
  sleep 1
done
echo "Postgres started"

pytest -s functional/