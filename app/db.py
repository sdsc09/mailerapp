import mysql.connector
import os
from urllib.parse import urlparse
from flask import g, current_app
from flask.cli import with_appcontext
import click

def get_db():
    if 'db' not in g:
        # Obtiene la URL de conexión desde la variable de entorno
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("La variable de entorno DATABASE_URL no está configurada")

        # Parsea la URL para extraer host, usuario, contraseña, etc.
        parsed = urlparse(url)

        g.db = mysql.connector.connect(
            host=parsed.hostname,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],  # quita la barra inicial del nombre de la base
            port=parsed.port or 3306
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    # Asegúrate de que el esquema esté definido
    from .schema import instructions
    for instruction in instructions:
        c.execute(instruction)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)