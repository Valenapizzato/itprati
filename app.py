from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# E-mail config
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL") == "True"

mail = Mail(app)

# Simples "banco de dados"
estagiarios = []
empresas = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro-estagiario', methods=['GET', 'POST'])
def cadastro_estagiario():
    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get("curriculo")
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            data["curriculo"] = filename
        estagiarios.append(data)
        send_email("Novo cadastro de estagiário", str(data))
        flash("Cadastro enviado com sucesso!")
        return redirect(url_for('cadastro_estagiario'))
    return render_template('form_estagiario.html')

@app.route('/cadastro-empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        data = request.form.to_dict()
        empresas.append(data)
        send_email("Novo cadastro de empresa", str(data))
        flash("Cadastro enviado com sucesso!")
        return redirect(url_for('cadastro_empresa'))
    return render_template('form_empresa.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['username'] == os.getenv("ADMIN_USER") and request.form['password'] == os.getenv("ADMIN_PASS"):
            session['admin'] = True
            return redirect(url_for('dashboard'))
        flash("Login inválido.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    return render_template('dashboard.html', estagiarios=estagiarios, empresas=empresas)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

def send_email(subject, body):
    msg = Message(subject, sender=os.getenv("MAIL_USERNAME"), recipients=["itpratiestagios@gmail.com"])
    msg.body = body
    mail.send(msg)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)