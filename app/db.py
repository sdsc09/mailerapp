import psycopg
import os
import psycopg2.extras
from flask import g, current_app
from .schema import instructions

import psycopg2.extras

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            dbname=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # 👈 clave
    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for instruction in instructions:
        c.execute(instruction)
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
