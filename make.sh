#! /bin/bash
#gunicorn -c gunicorn.py Flask:app
nohup python Flask.py > mylog.log 2>&1 &