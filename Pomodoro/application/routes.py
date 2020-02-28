# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from flask import current_app as app
import json

from datetime import datetime as dt


from .models import Task, State, db


@app.route('/')
def index():
    # TO DO tasks
    todo_tasks = [(task.id, task.creation_date.replace(microsecond=0), task.name) for task in db.session.query(Task).
        join(State, Task.state_id == State.id).
        filter_by(name='TODO').all()]
    # Show past tasks
    past_tasks = [(task.end_date.replace(microsecond=0), task.name, task.pomodoros) for task in db.session.query(Task).
        join(State, Task.state_id == State.id).
        filter_by(name='DONE').all()]
    # Current task
    task_id = request.args.get('id_current_task', '')
    if task_id:
        current_task_pomodoros = db.session.query(Task).filter_by(id=task_id).first().pomodoros
    else:
        current_task_pomodoros = ""

    return render_template('index.html', current_task_pomodoros=current_task_pomodoros, todo_tasks=todo_tasks, past_tasks=past_tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_creator']
    if task_name: # Ugly check error empty field
        state = db.session.query(State).filter_by(name='TODO').first()
        new_task = Task(name=task_name, state=state)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/drop_todo_tasks', methods=['POST'])
def drop_todo_tasks():
    todo_tasks = db.session.query(Task).join(State, Task.state_id == State.id).filter_by(name='TODO').all()
    for task in todo_tasks:
        db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_pomodoro', methods=['POST'])
def add_pomodoro():
    task_id = int(request.json['id_current_task'])
    db.session.query(Task).filter_by(id=task_id).update({'pomodoros': Task.pomodoros + 1})
    db.session.commit()

    # return redirect(url_for('index', id_current_task=task_id))
    pomodoros = db.session.query(Task).filter_by(id=task_id).first().pomodoros
    return json.dumps({'current_task_pomodoros': pomodoros, 'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/end_task', methods=['POST'])
def end_task():
    task_id = int(request.json['id_current_task'])
    current_task = db.session.query(Task).filter_by(id=task_id).first()
    if current_task.pomodoros:
        current_task.end_date = dt.utcnow()
        state = db.session.query(State).filter_by(name='DONE').first()
        state.tasks.append(current_task)

        db.session.commit()

    return redirect(url_for('index'))

# 1. Selected table. Hide id of each TO DO task. -> DONE
# 2. When click in work button, if not selected cell, show error message. When end work time, launch event to add a pomodoro in BD -> DONE
# 4. Upload file with to do tasks.
# 5. If task name is empty show error message. -> DONE
# 6. Button DONE to end task -> DONE
# 7. Past tasks with sorted by date, with date, name and pomodoros
# 8. Remove all pomodoros button
