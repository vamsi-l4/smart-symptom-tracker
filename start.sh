#!/bin/bash
# Render already sets PWD to src
exec uvicorn app:app --host 0.0.0.0 --port $PORT
