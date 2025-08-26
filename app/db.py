import psycopg
import os
from urllib.parse import urlparse
from flask import g
from .schema import instructions

def get_db():
    if 'db' not in g:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL no está configurada")
        # Usa sslmode=require para Render
        g.db = psycopg.connect(url, sslmode='require')
        g.c = g.db.cursor()
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
    # No agregamos el comando CLI porque usamos /init-db como ruta web