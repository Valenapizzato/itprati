from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecret'

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

from models import init_app, db, Estagiario, Empresa, Candidatura
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario-estagiario', methods=['GET', 'POST'])
def formulario_estagiario():
    if request.method == 'POST':
        dados = request.form.to_dict()
        senha_hash = generate_password_hash(dados.get('senha'))

        soft_skills = "; ".join([
            f"{i}: {request.form.get(f'soft_{i}', '0')}" for i in range(20)
        ])

        formatos = request.form.getlist("formato_trabalho")
        formato_trabalho = ", ".join(formatos)

        novo_estagiario = Estagiario(
            nome=dados.get('nome'),
            data_nascimento=dados.get('data_nascimento'),
            email=dados.get('email'),
            senha=senha_hash,
            telefone=dados.get('telefone'),
            cidade_estado=dados.get('cidade_estado'),
            curso=dados.get('curso'),
            instituicao=dados.get('instituicao'),
            disponibilidade=dados.get('disponibilidade'),
            github=dados.get('github'),
            habilidades=dados.get('habilidades'),
            area_interesse=dados.get('area_interesse'),
            experiencias=dados.get('experiencias'),
            soft_skills=soft_skills,
            endereco=dados.get('endereco'),
            formato_trabalho=formato_trabalho,
            quer_consultoria=dados.get('quer_consultoria')
        )
        db.session.add(novo_estagiario)
        db.session.commit()
        return render_template('confirmacao.html')
    return render_template('formulario_estagiario.html')

@app.route('/formulario-empresa', methods=['GET', 'POST'])
def formulario_empresa():
    if request.method == 'POST':
        dados = request.form.to_dict()
        senha_hash = generate_password_hash(dados.get('senha'))

        nova_empresa = Empresa(
            nome=dados.get('nome'),
            cnpj=dados.get('cnpj'),
            responsavel=dados.get('responsavel'),
            email=dados.get('email'),
            senha=senha_hash,
            telefone=dados.get('telefone'),
            areas_interesse=dados.get('areas_interesse'),
            requisitos=dados.get('requisitos'),
            tipo_contrato=dados.get('tipo_contrato'),
            beneficios=dados.get('beneficios'),
            cursos_exigidos=dados.get('cursos_exigidos'),
            endereco=dados.get('endereco'),
            modelo_servico=dados.get('modelo_servico')
        )
        db.session.add(nova_empresa)
        db.session.commit()
        return render_template('confirmacao_empresa.html')
    return render_template('form_empresa.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'admin':
            session['logado'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('login'))

    estagiarios = Estagiario.query.all()
    empresas = Empresa.query.all()

    return render_template('dashboard.html', estagiarios=estagiarios, empresas=empresas)

@app.route('/portal-estudante')
def portal_estudante():
    return render_template('portal_estudante.html')

@app.route('/portal-empresa')
def portal_empresa():
    return render_template('portal_empresa.html')

@app.route('/login-estudante', methods=['GET', 'POST'])
def login_estudante():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not email or '@' not in email:
            return render_template('login_estudante.html', erro='Email inválido.')

        estagiario = Estagiario.query.filter_by(email=email).first()
        if estagiario and check_password_hash(estagiario.senha, senha):
            session['estudante_email'] = estagiario.email

            candidaturas = Candidatura.query.filter_by(estagiario_id=estagiario.id).all()
            qtd_candidaturas = len(candidaturas)

            return render_template(
                'painel_estudante.html',
                nome=estagiario.nome,
                email=estagiario.email,
                curso=estagiario.curso,
                instituicao=estagiario.instituicao,
                telefone=estagiario.telefone,
                cidade=estagiario.cidade_estado,
                github=estagiario.github,
                habilidades=estagiario.habilidades,
                area_interesse=estagiario.area_interesse,
                disponibilidade=estagiario.disponibilidade,
                experiencias=estagiario.experiencias,
                formato_trabalho=estagiario.formato_trabalho,
                quer_consultoria=estagiario.quer_consultoria,
                soft_skills=estagiario.soft_skills or '',
                empresas=Empresa.query.all(),
                qtd_candidaturas=qtd_candidaturas
            )
        else:
            return render_template('login_estudante.html', erro='Email ou senha incorretos.')

    return render_template('login_estudante.html')

@app.route('/login-empresa', methods=['GET', 'POST'])
def login_empresa():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        empresa = Empresa.query.filter_by(email=email).first()
        if empresa and check_password_hash(empresa.senha, senha):
            candidaturas = Candidatura.query.filter_by(empresa_id=empresa.id).all()
            estagiarios = [Estagiario.query.get(c.estagiario_id) for c in candidaturas]

            return render_template(
                'painel_empresa.html',
                empresa=empresa.nome,
                email=empresa.email,
                responsavel=empresa.responsavel,
                estagiarios=estagiarios,
                cnpj=empresa.cnpj,
                telefone=empresa.telefone,
                endereco=empresa.endereco,
                areas_interesse=empresa.areas_interesse,
                requisitos=empresa.requisitos,
                beneficios=empresa.beneficios,
                cursos_exigidos=empresa.cursos_exigidos,
                modelo_servico=empresa.modelo_servico
            )
        else:
            return render_template('login_empresa.html', erro='Email ou senha incorretos.')
    return render_template('login_empresa.html')

@app.route('/candidatar/<int:id_empresa>', methods=['POST'])
def candidatar(id_empresa):
    if 'estudante_email' not in session:
        return redirect(url_for('login_estudante'))

    estagiario = Estagiario.query.filter_by(email=session['estudante_email']).first()
    empresa = Empresa.query.get(id_empresa)

    if not estagiario or not empresa:
        return "Estagiário ou empresa não encontrados", 404

    nova = Candidatura(estagiario_id=estagiario.id, empresa_id=empresa.id)
    db.session.add(nova)
    db.session.commit()

    msg = Message(
        subject="Novo candidato para sua vaga no ITpraTI!",
        recipients=[empresa.email],
        body=f"Olá {empresa.responsavel},\n\n"
             f"O estagiário {estagiario.nome} se candidatou à sua vaga.\n"
             f"Email do estudante: {estagiario.email}\n"
             f"Área de interesse: {estagiario.area_interesse}\n"
             f"GitHub/Portfólio: {estagiario.github}\n"
             f"Disponibilidade: {estagiario.disponibilidade}\n\n"
             f"Acesse o painel da empresa para ver mais detalhes: https://itprati.onrender.com/login-empresa"
    )
    mail.send(msg)

    return redirect(url_for('painel_estudante'))

@app.route('/editar-estudante', methods=['GET', 'POST'])
def editar_estudante():
    email = session.get('estudante_email')
    est = Estagiario.query.filter_by(email=email).first()
    if not est:
        return redirect(url_for('login_estudante'))

    if request.method == 'POST':
        est.nome = request.form['nome']
        est.email = request.form['email']
        est.curso = request.form['curso']
        est.instituicao = request.form['instituicao']
        est.telefone = request.form['telefone']
        est.cidade_estado = request.form['cidade_estado']
        est.github = request.form['github']
        est.area_interesse = request.form['area_interesse']
        est.formato_trabalho = request.form['formato_trabalho']
        est.quer_consultoria = request.form['quer_consultoria']
        est.experiencias = request.form['experiencias']
        db.session.commit()
        return redirect(url_for('login_estudante'))

    return render_template('editar_estudante.html', est=est)

@app.route('/editar-empresa', methods=['GET', 'POST'])
def editar_empresa():
    email = session.get('empresa_email')
    emp = Empresa.query.filter_by(email=email).first()
    if not emp:
        return redirect(url_for('login_empresa'))

    if request.method == 'POST':
        emp.nome = request.form['nome']
        emp.email = request.form['email']
        emp.cnpj = request.form['cnpj']
        emp.responsavel = request.form['responsavel']
        emp.telefone = request.form['telefone']
        emp.endereco = request.form['endereco']
        emp.areas_interesse = request.form['areas_interesse']
        emp.requisitos = request.form['requisitos']
        emp.beneficios = request.form['beneficios']
        emp.cursos_exigidos = request.form['cursos_exigidos']
        emp.modelo_servico = request.form['modelo_servico']
        db.session.commit()
        return redirect(url_for('login_empresa'))

    return render_template('editar_empresa.html', emp=emp)
@app.route('/ppa/<int:id_estagiario>')
def ppa_estagiario(id_estagiario):
    est = Estagiario.query.get_or_404(id_estagiario)
    return render_template('ppa.estagiario.html', est=est)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)