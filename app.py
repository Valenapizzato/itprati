from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

CSV_FILE = 'cadastros_estagiarios.csv'

@app.route('/')
def index():
    return redirect(url_for('formulario_estagiario'))

@app.route('/formulario-estagiario', methods=['GET', 'POST'])
def formulario_estagiario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        curso = request.form['curso']
        soft_skills = ', '.join(request.form.getlist('soft_skills'))

        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Nome', 'Email', 'Curso', 'Soft Skills'])
            writer.writerow([nome, email, curso, soft_skills])

        return render_template('confirmacao.html', nome=nome, email=email, curso=curso, soft_skills=soft_skills)
    return render_template('formulario_estagiario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'admin':
            session['logado'] = True
            return redirect(url_for('painel'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/painel')
@app.route('/cadastro-empresa', methods=['GET', 'POST'])
def cadastro_empresa():
    if request.method == 'POST':
        empresa = request.form['empresa']
        contato = request.form['contato']
        email = request.form['email']

        file_exists = os.path.isfile('cadastros_empresas.csv')
        with open('cadastros_empresas.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Empresa', 'Contato', 'Email'])
            writer.writerow([empresa, contato, email])

        return render_template('confirmacao_empresa.html', empresa=empresa, contato=contato, email=email)
    return render_template('cadastro_empresa.html')

@app.route('/painel')
def painel():
    if not session.get('logado'):
        return redirect(url_for('login'))

    dados = []
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            dados = list(reader)
    else:
        headers = []

        empresas = []
    if os.path.isfile('cadastros_empresas.csv'):
        with open('cadastros_empresas.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            empresas = list(reader)
    return render_template('painel.html', headers=headers, dados=dados, empresas=empresas)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
