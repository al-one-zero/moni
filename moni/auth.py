import functools, sys
from werkzeug.security import check_password_hash, generate_password_hash
from moni import login_required
from moni.db import get_db
from flask import Blueprint, render_template, session, g, request, flash, redirect, url_for

bp = Blueprint('auth', __name__, url_prefix='/auth')

log = lambda s, p='': print(p, s, file=sys.stdout)
logerr = lambda s, p='': print(p, s, file=sys.stderr)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        error = None

        log(username, 'request :')
        if username is None:
            error = 'No username provided'
        elif password is None:
            error = 'No password provided'
        elif db.execute('select user_id from user where username = ?', (username,)).fetchone() is not None:
            error = 'Username already taken'
        else:
            db.execute('insert into user(username, password) values(?, ?)', (username, generate_password_hash(password, )))
            db.commit()
            log('user created')
            return redirect(url_for('auth.login'))

        logerr(error, 'error')
    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        error = None

        g.user = get_db().execute('select * from user where username = ?', (username, )).fetchone()
        if not g.user:
            error = 'wrong username'
        else:
            if not check_password_hash(g.user['password'], password):
                error = 'wrong password'
        
        if error is None:
            session.clear()
            session['user_id'] = g.user['user_id']
            log(g.user['admin'])
            return redirect(url_for('user.dboard'))
        else:
            logerr(error, 'error : ')


    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('select * from user where user_id = ?', (user_id,)).fetchone()
