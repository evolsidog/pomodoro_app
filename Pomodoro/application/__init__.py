# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, event

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    # Configuration - In this case we don't use configuration file
    app.debug = True
    db_path = os.path.join(os.path.dirname(__file__), 'pomodoro.db')
    db_uri = 'sqlite:///{}'.format(db_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Imports
        from . import routes
        from . import models

        # Add catalogue of states
        @event.listens_for(models.State.__table__, 'after_create')
        def insert_initial_values(*args, **kwargs):
            states = [models.State(name=state) for state in ['TODO', 'WP', 'DONE']]
            db.session.add_all(states)
            db.session.commit()

        # Create tables for our models
        db.create_all()

        return app
