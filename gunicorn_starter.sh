#!/bin/bash
gunicorn --chdir app web_app:app -w 2 --threads 2 -b 0.0.0.0:8003