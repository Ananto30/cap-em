#!/bin/bash
docker build --build-arg db_url=postgres://capem:pass@192.168.0.107:5432/postgres -t capem/flask . 