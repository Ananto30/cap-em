#!/bin/bash
mkdir ./app/config
cp ./config/config.txt ./app/config/
gunicorn --chdir app web_app:app -w 2 --threads 2 -b 0.0.0.0:8003