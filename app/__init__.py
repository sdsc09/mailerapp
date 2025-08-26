import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'  # Necesario para flash()

    # Configuración desde variables de entorno
    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
        FROM_EMAIL=os.environ.get('FROM_EMAIL')
    )

    # Inicializa la base de datos
    from . import db
    db.init_app(app)

    # Registra el blueprint
    from . import mail
    app.register_blueprint(mail.bp)

    # Ruta para inicializar la base de datos
    @app.route('/init-db')
    def init_db_route():
        db.init_db()
        return "Base de datos inicializada. La tabla 'email' ha sido creada."

    return app
