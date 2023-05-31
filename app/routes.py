from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user
from werkzeug.security import check_password_hash
from . import login_manager
from .user_model import User
import csv
import os

bp = Blueprint('routes', __name__)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('routes.login'))

        login_user(user, remember=remember)
        return redirect(url_for('routes.index'))

    return render_template('login.html')


@bp.route('/')
@login_required
def index():
    tasks = []
    with open('articles_summary.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return render_template('index.html', tasks=tasks)

@bp.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    title = request.form['title']
    with open('articles_summary.csv', 'r') as f:
        tasks = list(csv.DictReader(f))
    tasks = [task for task in tasks if task['title'] != title]
    with open('articles_summary.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)
    return redirect(url_for('index'))

@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        new_task = {key: request.form[key] for key in request.form}
        with open('articles_summary.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=new_task.keys())
            writer.writerow(new_task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@bp.route('/edit_task/<title>', methods=['GET', 'POST'])
@login_required
def edit_task(title):
    with open('articles_summary.csv', 'r') as f:
        tasks = list(csv.DictReader(f))
    task_to_edit = [task for task in tasks if task['title'] == title][0]
    if request.method == 'POST':
        for key in request.form:
            task_to_edit[key] = request.form[key]
        tasks = [task if task['title'] != title else task_to_edit for task in tasks]
        with open('articles_summary.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
            writer.writeheader
