#!/bin/bash

echo "Current directory: $(pwd)"
echo "Environment variables:"
env

# Run FastAPI from current directory with PYTHONPATH set
PYTHONPATH=. uvicorn app:app --host 0.0.0.0 --port $PORT
