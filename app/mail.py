from flask import Blueprint, render_template, request, flash, url_for, redirect, current_app
import sendgrid
from sendgrid.helpers.mail import Mail as SendGridMail, Email, To, Content
from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    db, c = get_db()

    if search:
        query = "SELECT * FROM email WHERE email ILIKE %s"
        c.execute(query, (f'%{search}%',))
    else:
        c.execute("SELECT * FROM email")

    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Email es obligatorio')
        if not subject:
            errors.append('Asunto es obligatorio')
        if not content:
            errors.append('Contenido es obligatorio')

        if len(errors) == 0:
            print("✅ No hay errores. Intentando guardar correo...")
            print(f"Datos: email={email}, subject={subject}, content={content}")
            try:
                send_email(email, subject, content)
                db, c = get_db()
                print("Conexión a DB obtenida")
                c.execute(
                    "INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)",
                    (email, subject, content)
                )
                db.commit()
                print("✅ Correo guardado en la base de datos")
                flash("Correo enviado y guardado correctamente")
                return redirect(url_for('mail.index'))
            except Exception as e:
                print("❌ Error al guardar el correo:", e)
                flash(f"Error al guardar el correo: {str(e)}")
        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')

def send_email(to, subject, content):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
        from_email = Email(current_app.config['FROM_EMAIL'])
        to_email = To(to)
        content = Content('text/plain', content)
        mail = SendGridMail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print("SendGrid response:", response.status_code)
    except Exception as e:
        print("Error al enviar correo:", e)

