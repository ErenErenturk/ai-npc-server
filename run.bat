@echo off
call .venv\Scripts\activate
pip install -r requirements.txt
python server.py
pause
