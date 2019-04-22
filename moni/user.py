import sys
from collections import namedtuple
from flask import Blueprint, g, render_template, request, redirect, url_for, abort
from moni.db import get_db
from moni.auth import login_required 

bp = Blueprint('user', __name__, url_prefix="/u")

Project = namedtuple('Project', 'id, owner, name, location, s_date, e_date')
Expanse = namedtuple('Expanse', 'id, pj_id, cat, curr, value, label, ts')
Currency = namedtuple('Currency', 'id, name, ex_rate')

@bp.before_app_request
def load_currencies():
    g.currencies = [Currency._make(tuple(c)) 
                    for c in get_db().execute(
                        'select * from currency order by curr_id').fetchall()]

# Projects management
@bp.route('/', methods=('GET', 'POST'))
@login_required
def u_index():
    return redirect(url_for('user.dboard'))

@bp.route('dashboard', methods=('GET', 'POST'))
@login_required
def dboard():
    db = get_db()

    pjs = []
    fetched_pjs = db.execute('select * from project where owner_id = ?', (g.user['user_id'],)).fetchall()
    for pj in fetched_pjs:

        pjs.append(Project._make(tuple(pj)))
    
    if request.method == "POST":
        name = request.form['pj_name']
        db.execute('insert into project(owner_id, name) values(?, ?)', (g.user['user_id'], name))
        db.commit()
        return redirect(url_for('user.dboard'))
    return render_template('dboard.html', pjs = pjs)

@bp.route('pj/<int:pj_id>/overview', methods=('GET', 'POST'))
def pj_overview(pj_id):
    db = get_db()
    pj = Project._make(tuple(db.execute('select * from project where pj_id = ?', (pj_id,)).fetchone()))
    exps = [Expanse._make(tuple(e)) 
                for e in db.execute(
                'select * from expanse where pj_id = ? order by timestamp desc', (pj_id,)).fetchall()]
    return render_template('pj.html', pj = pj, exps = exps)

def get_pj(pj_id, check_owner=True):
    db = get_db()
    pj = db.execute('select * from project where pj_id = ?', (pj_id,)).fetchone()

    if pj is None:
        return abort(404, "project {} doesn't exist.".format(pj_id))
    
    if check_owner and pj['owner_id'] != g.user['user_id']:
        return abort(403)
    
    return pj

@bp.route('pj/<int:pj_id>/delete', methods=('POST',))
@login_required
def delete_pj(pj_id):
    _ = get_pj(pj_id) # useful to check the ownership of the project
    db = get_db()
    db.execute('delete from expanse where pj_id = ?', (pj_id,))
    db.execute('delete from project where pj_id = ?', (pj_id,))
    db.commit()
    return redirect(url_for('user.dboard'))

@bp.route('add')
@login_required
def add_pj():
    return 'add view'

@bp.route('settings')
@login_required
def settings():
    return render_template('settings.html')

@bp.route('admin')
@login_required
def admin():
    if not g.user['admin']:
        return abort(403)
    return render_template('admin.html')

# Exapnses management

@bp.route('/pj/<int:pj_id>/add', methods=('POST',))
@login_required
def add_exp(pj_id):
    _ = get_pj(pj_id)
    db = get_db()
    exp = request.form
    # get curr_id
    curr_id = 1
    db.execute('insert into expanse(pj_id, label, value, curr, cat) values(?, ?, ?, ?, ?)',
                (pj_id, exp['label'], exp['value'], curr_id, exp['cat']))
    db.commit()

    return redirect(url_for('user.pj_overview', pj_id = pj_id))
