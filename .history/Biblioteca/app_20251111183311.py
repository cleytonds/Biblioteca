# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, User, Livro
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- FORMULÁRIOS ----------
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 100)])
    confirmar = PasswordField('Confirmar Senha', validators=[EqualTo('senha', 'Senhas diferentes')])
    is_admin = BooleanField('Registrar como Administrador')

class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor')
    ano = IntegerField('Ano')
    descricao = TextAreaField('Descrição')

# ---------- ROTAS ----------
@app.before_first_request
def criar_tabelas():
    db.create_all()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.senha.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout feito.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email já cadastrado.', 'warning')
            return redirect(url_for('register'))
        user = User(nome=form.nome.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.senha.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# -------- CRUD de LIVROS --------
@app.route('/livros')
@login_required
def listar_livros():
    livros = Livro.query.all()
    return render_template('livros/lista.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if not current_user.is_admin:
        flash('Somente administradores podem adicionar livros.', 'danger')
        return redirect(url_for('listar_livros'))
    form = LivroForm()
    if form.validate_on_submit():
        livro = Livro(titulo=form.titulo.data, autor=form.autor.data, ano=form.ano.data, descricao=form.descricao.data)
        db.session.add(livro)
        db.session.commit()
        flash('Livro adicionado!', 'success')
        return redirect(url_for('listar_livros'))
    return render_template('livros/novo.html', form=form)

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    if not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('listar_livros'))
    form = LivroForm(obj=livro)
    if form.validate_on_submit():
        livro.titulo = form.titulo.data
        livro.autor = form.autor.data
        livro.ano = form.ano.data
        livro.descricao = form.descricao.data
        db.session.commit()
        flash('Livro atualizado!', 'success')
        return redirect(url_for('listar_livros'))
    return render_template('livros/editar.html', form=form, livro=livro)

@app.route('/livros/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    if not current_user.is_admin:
        flash('Somente administradores podem excluir livros.', 'danger')
        return redirect(url_for('listar_livros'))
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro removido.', 'info')
    return redirect(url_for('listar_livros'))

@app.before_first_request
def criar_tabelas():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
