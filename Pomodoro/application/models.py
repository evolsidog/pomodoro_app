# -*- coding: utf-8 -*-
from datetime import datetime

from . import db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='state', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    pomodoros = db.Column(db.Integer, unique=False, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, unique=False, nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'),
        nullable=False)
