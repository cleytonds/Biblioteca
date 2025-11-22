# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, User, Book
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Forms
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 128)])
    password2 = PasswordField('Confirme', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Registrar como administrador')

class BookForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor')
    ano = IntegerField('Ano')
    descricao = TextAreaField('Descrição')

# app factory
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

# páginas públicas
@app.route('/')
def index():
    return render_template('index.html')

# registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Usuário já existe.')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrado com sucesso. Faça login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login realizado.')
            return redirect(url_for('lista_livros'))
        flash('Usuário ou senha inválidos.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Desconectado.')
    return redirect(url_for('index'))

# CRUD de livros
@app.route('/livros')
@login_required
def lista_livros():
    livros = Book.query.all()
    return render_template('livros/lista.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    # só admin pode criar (exemplo)
    if not current_user.is_admin:
        flash('Acesso negado: somente administradores podem adicionar livros.')
        return redirect(url_for('lista_livros'))

    form = BookForm()
    if form.validate_on_submit():
        livro = Book(titulo=form.titulo.data, autor=form.autor.data, ano=form.ano.data, descricao=form.descricao.data)
        db.session.add(livro)
        db.session.commit()
        flash('Livro adicionado.')
        return redirect(url_for('lista_livros'))
    return render_template('livros/novo.html', form=form)

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('lista_livros'))
    livro = Book.query.get_or_404(id)
    form = BookForm(obj=livro)
    if form.validate_on_submit():
        livro.titulo = form.titulo.data
        livro.autor = form.autor.data
        livro.ano = form.ano.data
        livro.descricao = form.descricao.data
        db.session.commit()
        flash('Livro atualizado.')
        return redirect(url_for('lista_livros'))
    return render_template('livros/editar.html', form=form, livro=livro)

@app.route('/livros/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('lista_livros'))
    livro = Book.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro excluído.')
    return redirect(url_for('lista_livros'))

if __name__ == '__main__':
    app.run(debug=True)
