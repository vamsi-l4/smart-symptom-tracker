#!/bin/bash

# Run FastAPI from project root
exec uvicorn src.app:app --host 0.0.0.0 --port $PORT
