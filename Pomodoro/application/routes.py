# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from flask import current_app as app

from .models import Task, State, db


@app.route('/')
def index():
    # TO DO tasks
    todo_tasks = [(task.id, task.name) for task in db.session.query(Task).
        join(State, Task.state_id == State.id).
        filter_by(name='TODO').all()]
    # Show past tasks
    past_tasks = [task.name for task in db.session.query(Task).
        join(State, Task.state_id == State.id).
        filter_by(name='DONE').all()]
    # past_tasks = [task.name for task in Task.query.filter_by(state='DONE').all()]
    return render_template('index.html', todo_tasks=todo_tasks, past_tasks=past_tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_creator']
    state = db.session.query(State).filter_by(name='TODO').first()
    new_task = Task(name=task_name, state=state)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# 1. Selected table. Hide id of each TO DO task.
# 2. When click en work, if not selected cell, show error message. When end work time, launch event to add a pomodoro in BD