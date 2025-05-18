#!/bin/bash
source .venv/bin/activate
pip install -r requirements.txt
python server.py
read -n 1 -s
