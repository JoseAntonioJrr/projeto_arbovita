from flask import Flask, request, send_from_directory, jsonify
import os
import sqlite3

# Define o diretório raiz do projeto e o diretório de templates
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
DB_PATH = os.path.join(PROJECT_ROOT, 'database.db')

# Desativa a pasta estática padrão do Flask
app = Flask(__name__, static_folder=None)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Tabela de Usuários
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    # Tabela de Mensagens de Contato
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Tabela de Newsletter
    conn.execute('''
        CREATE TABLE IF NOT EXISTS newsletter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar
init_db()

# Configuração para servir a página inicial
@app.route('/')
def serve_index():
    return send_from_directory(TEMPLATE_DIR, 'index.html')

# Rota genérica para servir arquivos estáticos e páginas HTML
@app.route('/<path:path>')
def serve_static(path):
    # 1. Primeiro tenta servir arquivos estáticos (CSS, JS, Imagens) da raiz do projeto
    # Ex: assets/css/main.css, mapa-arborizacao-belem/arvore.png
    full_path_root = os.path.join(PROJECT_ROOT, path)
    if os.path.exists(full_path_root) and os.path.isfile(full_path_root):
        return send_from_directory(PROJECT_ROOT, path)
    
    # 2. Se não for estático, tenta buscar nos templates (arquivos HTML movidos)
    # Ex: about.html
    full_path_template = os.path.join(TEMPLATE_DIR, path)
    if os.path.exists(full_path_template) and os.path.isfile(full_path_template):
        return send_from_directory(TEMPLATE_DIR, path)

    # 3. Tenta adicionar a extensão .html se o usuário digitou sem (ex: /about)
    if os.path.exists(full_path_template + '.html'):
         return send_from_directory(TEMPLATE_DIR, path + '.html')
    
    # Log de erro no terminal para ajudar a depurar
    print(f"[404] Arquivo não encontrado: {path}")
    return "Arquivo não encontrado", 404

# --- Novas APIs em Python ---

@app.route('/api/contact', methods=['POST'])
def contact_api():
    """
    Substitui forms/contact.php
    Recebe: name, email, subject, message
    """
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        conn = get_db_connection()
        conn.execute('INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                     (name, email, subject, message))
        conn.commit()
        conn.close()
        
        # O frontend espera EXATAMENTE a string "OK" para mostrar a mensagem de sucesso
        return "OK" 
    except Exception as e:
        return str(e), 500

@app.route('/api/register', methods=['POST'])
def register_api():
    """
    Nova API para cadastro de usuários
    Recebe: nome, email, usuario, senha
    """
    try:
        data = request.form
        name = data.get('nome')
        email = data.get('email')
        username = data.get('usuario')
        password = data.get('senha')

        if not all([name, email, username, password]):
            return jsonify({"success": False, "message": "Todos os campos são obrigatórios."}), 400

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)',
                         (name, email, username, password))
            conn.commit()
            success = True
            msg = "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError:
            success = False
            msg = "Email ou usuário já cadastrado."
        finally:
            conn.close()
        
        # Retorna JSON para o frontend processar
        if success:
            return jsonify({"success": True, "message": msg})
        else:
            return jsonify({"success": False, "message": msg}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login_api():
    """
    Nova API para login de usuários
    Recebe: usuario, senha (ou email, senha)
    """
    try:
        data = request.form
        # O formulário envia 'email' no campo id='email_login' mas name='email'.
        # O JS envia o FormData.
        # Vamos checar se o login é por email ou usuário, ou simplificar.
        # O HTML tem name='email', então vamos usar email.
        email_input = data.get('email') 
        password_input = data.get('senha')
        
        # Fallback: se o JS enviar 'usuario' em vez de email
        user_input = data.get('usuario')
        
        login_identifier = email_input if email_input else user_input

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? OR username = ?', (login_identifier, login_identifier)).fetchone()
        conn.close()

        if user and user['password'] == password_input:
             # Retorna sucesso, o nome do usuário e o email para salvar no navegador
            return jsonify({"success": True, "username": user['username'], "email": user['email']})
        else:
            return jsonify({"success": False, "message": "Credenciais inválidas."}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/update_profile', methods=['POST'])
def update_profile_api():
    """
    Simula a atualização de dados do usuário
    """
    try:
        # Simplificação: Não vamos implementar update real sem autenticação de sessão real
        return jsonify({"success": True, "message": "Dados atualizados! (Simulação)"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe_api():
    """
    Simula o processamento de pagamento
    """
    try:
        print("--- Nova Assinatura Processada ---")
        # Aqui entraria a lógica do Stripe/PagSeguro
        return jsonify({"success": True, "message": "Pagamento confirmado!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/newsletter', methods=['POST'])
def newsletter_api():
    """
    Substitui forms/newsletter.php
    Recebe: email
    """
    try:
        data = request.form
        email = data.get('email')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO newsletter (email) VALUES (?)', (email,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Já inscrito, mas retorna OK para não dar erro no front
        finally:
            conn.close()
        
        return "OK"
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True, port=5000)
