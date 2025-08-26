import psycopg2
import os
from urllib.parse import urlparse
from flask import g

def get_db():
    if 'db' not in g:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL no está configurada")
        connection = psycopg2.connect(url, sslmode='require')
        g.db = connection
        g.c = connection.cursor()
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)