#configurações do python
import os 
basedir = os.path.abspath(os.path.dirname(__file__))


class confing:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'troque_esta_chave_para_producao'
    #SQlite (arquivo Local)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'databese.bd')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    