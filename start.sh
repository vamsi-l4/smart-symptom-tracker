#!/bin/bash
# Ensure we are in the src directory
cd src
exec uvicorn app:app --host 0.0.0.0 --port $PORT
