import psycopg
import os
import psycopg2.extras
from flask import g, current_app
from .schema import instructions

import psycopg2.extras

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            "postgresql://mailerapp_db_user:kgrSR6CA1TL1SvjyZ2umzEYDgHMOZU5Y@dpg-d2n2pvffte5s73bfauhg-a/mailerapp_db"
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
