#!/usr/bin/env python

import sqlite3
from flask import g

import flasking 

def connect_db():
    return sqlite3.connect(flasking.app.config['DATABASE'])

def init_db():
    with flasking.app.app_context():
        db = get_db()
        with flasking.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

