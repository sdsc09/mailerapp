import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para flash()

    # Configuración desde variables de entorno
    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        FROM_EMAIL=os.environ.get('FROM_EMAIL')
    )

    # Importa y registra el blueprint
    from . import db
    db.init_app(app)

    from . import mail
    app.register_blueprint(mail.bp)

    # Ruta directa en la app principal para /init-db
    @app.route('/init-db')
    def init_db_route():
        db.init_db()
        return "✅ Base de datos inicializada. La tabla 'email' ha sido creada."

    # Ruta raíz, por si alguien entra directamente
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('mail.index'))

    return app