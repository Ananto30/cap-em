#!/bin/bash
docker run --name capem -v $(pwd)/config:/app/config -p 8003:8003 capem/flask