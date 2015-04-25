#!/usr/bin/env python

from flask import request, session, redirect, url_for, abort, render_template, flash, Blueprint
from flasking.db.database import query_db, get_db 
from flasking import app



views = Blueprint('views', __name__, template_folder='../templates/views')

@views.route('/')
def show_entries():
    entries = query_db('select title, text from entries order by id desc')
    return render_template('show_entries.html', entries=entries)

@views.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    query_db('insert into entries (title, text) values (?, ?)',
                 args=[request.form['title'], request.form['text']])
    get_db().commit()
    flash('New entry was successfully posted')
    return redirect(url_for('views.show_entries'))

@views.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('views.show_entries'))
    return render_template('login.html', error=error)

@views.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('views.show_entries'))