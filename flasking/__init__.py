#!/usr/bin/env python


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

from flasking.db.database import connect_db, query_db, get_db 


# configuration
DATABASE = '/tmp/flasking.db'
DEBUG = True
SECRET_KEY = '5h1pp3r143r'
USERNAME = 'admin'
PASSWORD = 'default'


# application
app = Flask(__name__)
app.config.from_object(__name__)

from flasking.views.views import views

app.register_blueprint(views)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

