#!/usr/bin/env python3
from flask import request, session, make_response, send_file
from flask_restful import Resource
from sqlalchemy import or_

from config import app, db, api
from models import User, Image, Guitar, Model

@app.route('/')
def index():
    return '<h1>service-tracker-server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

