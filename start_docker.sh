#!/bin/bash
docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 -e DB_URI=postgres://capem:pass@0.0.0.0:5432/postgres capem/flask