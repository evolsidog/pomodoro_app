# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from flask import current_app as app

from .models import Task, State, db


@app.route('/')
def index():
    # TO DO tasks
    todo_tasks = [(task.id, task.creation_date.replace(microsecond=0), task.name) for task in db.session.query(Task).
        join(State, Task.state_id == State.id).
        filter_by(name='TODO').all()]
    # Show past tasks
    past_tasks = [(task.end_date, task.name, task.run) for task in db.session.query(Task).
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
# 3. Upload file with to do tasks.
# 4. If task name is empty show error message.
# 5. Past tasks with sorted by date, with date, name and pomodoros.