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


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    entries = query_db('select title, text from entries order by id desc')
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    query_db('insert into entries (title, text) values (?, ?)',
                 args=[request.form['title'], request.form['text']])
    get_db().commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()    