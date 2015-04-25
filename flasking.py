#!/usr/bin/env python

import sqlite3
from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flasking.db'
DEBUG = True
SECRET_KEY = '5h1pp3r143r'
USERNAME = 'admin'
PASSWORD = 'default'


# application
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
# handy func
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()    