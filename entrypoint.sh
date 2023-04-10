#!/bin/bash
python3 -m src.create_table
uvicorn src.asgi:app