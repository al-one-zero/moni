from flask import Blueprint, g, render_template, request, redirect, url_for
from moni.db import get_db
from moni.auth import login_required 

bp = Blueprint('user', __name__, url_prefix="/u")

class Project():
    def __init__(self, pj):
        self.id = pj['pj_id']
        self.name = pj['name']
        self.location = pj['location']
        self.s_date = pj['start_date']
        self.e_date = pj['end_date']

@bp.route('dashboard', methods=('GET', 'POST'))
@login_required
def dboard():
    db = get_db()

    pjs = []
    fetched_pjs = db.execute('select * from project where owner_id = ?', (g.user['user_id'],)).fetchall()
    for pj in fetched_pjs:
        pjs.append(Project(pj))
    
    if request.method == "POST":
        name = request.form['pj_name']
        db.execute('insert into project(owner_id, name) values(?, ?)', (g.user['user_id'], name))
        db.commit()
        return redirect(url_for('user.dboard'))
    return render_template('dboard.html', pjs = pjs)

@bp.route('pj/<int:pj_id>/overview', methods=('GET', 'POST'))
def pj_overview(pj_id):
    db = get_db()
    pj = Project(db.execute('select * from project where pj_id = ?', (pj_id,)).fetchone())
    return render_template('pj.html', pj = pj)

@bp.route('add')
def add():
    return 'add view'

@bp.route('settings')
def settings():
    return render_template('settings.html')

@bp.route('admin')
def admin():
    if not g.user['admin']:
        return 'forbidden'
    return 'admin panel'