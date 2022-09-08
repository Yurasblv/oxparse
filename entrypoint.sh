#!/usr/bin/env bash
flask db init
flask db migrate
flask db upgrade
flask --app app.py --debug run --host=0.0.0.0
