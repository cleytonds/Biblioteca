# config.py
import os

class Config:
    SECRET_KEY = 'chave_secreta_trocar'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/biblioteca_db'
    # troque 'root' e senha '' pelos seus dados do MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
