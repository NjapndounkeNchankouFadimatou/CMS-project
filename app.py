from flask import Flask , render_template
from db import dBase
from flask_migrate import Migrate  # pour mettre a jour le smodifs faites sur la table 
from dotenv import load_dotenv
from auth.routes import auth
from user.routes_user import user
import os

app = Flask(__name__)

#configuration de l'app avec la base de donnee
load_dotenv('.env.local')#to load secret key var from .env.local
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') #config de la DBMS choisi et aussi le fichier avec les donnee
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SECRET_KEY'] = 'a9de8a3f91b8b02a633e10c243d473dd333e511f99ffe7711b72e0454cab11d3'
dBase.init_app(app) # lien entre bd et app
migration = Migrate(app, dBase)

app.register_blueprint(auth , url_prefix="/authentification")
app.register_blueprint(user , url_prefix="/user")

@app.route('/')
def create() :
    return render_template('auth/register.html')


if __name__ == '__main__':
    app.run(debug=True)