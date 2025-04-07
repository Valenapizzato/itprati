# ITpraTI - Plataforma de Conexão entre Estudantes de TI e Empresas

## Como rodar localmente:

1. Clone o repositório:
```bash
git clone https://github.com/Valenapizzato/itprati_site.git
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o `.env` com base no `.env.example`.

5. Rode a aplicação:
```bash
python app.py
```

## Como publicar no Render

1. Suba o projeto no GitHub.
2. Crie um novo Web Service no [Render](https://render.com).
3. Defina a branch e build command:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
4. Adicione as variáveis de ambiente manualmente.
5. Publique!

Pronto! Seu site estará online. 🚀