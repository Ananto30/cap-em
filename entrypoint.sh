#!/bin/bash
python3 -m src.create_table
uvicorn src.asgi:app --host 0.0.0.0 --port 8000 --workers 4