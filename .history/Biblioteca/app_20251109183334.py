from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_super_secreta"


# 1Função para conectar ao banco de dados MySQL

def conectar():
    return mysql.connector.connect(
        host="localhost",       # ou 127.0.0.1
        user="cleytonds",            # coloque o seu usuário do MySQL
        password="G1g2f3.vida",   # troque pela sua senha
        database="biblioteca_db"
    )

# 2 Página inicial (login)

@app.route('/')
def index():
    if 'usuario' in session:
        if session['tipo'] == 'admin':
            return redirect(url_for('admin_pagina'))
        else:
            return redirect(url_for('biblioteca'))
    return render_template('login.html')


# 3 Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Verifique no banco de dados
        if usuario == 'admin' and senha == '123':
            return redirect('/dashboard')
        else:
            return "Usuário ou senha incorretos"

    # Se for GET, apenas mostra a página
    return render_template('login.html')

# 4 Página do usuário comum

@app.route('/biblioteca')
def biblioteca():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    if session['tipo'] != 'usuario':
        return "<h3 style='color:red;'>Acesso negado! Apenas usuários comuns.</h3>"
    return render_template('biblioteca.html', usuario=session['usuario'])


# 5 Página do administrador

@app.route('/admin')
def admin_pagina():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    if session['tipo'] != 'admin':
        return "<h3 style='color:red;'>Acesso negado! Apenas administradores.</h3>"
    return render_template('admin.html', usuario=session['usuario'])


# 6 Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 7 Executar o servidor

if __name__ == '__main__':
    app.run(debug=True)
