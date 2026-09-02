from flask import Flask , render_template
from db import dBase
from flask_migrate import Migrate  # pour mettre a jour le smodifs faites sur la table 
from model import Article, User, Category,Contenu
app = Flask(__name__)

#configuration de l'app avec la base de donnee
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db" #config de la DBMS choisi et aussi le fichier avec les donnee
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
dBase.init_app(app) # lien entre bd et app
migration = Migrate(app, dBase)


@app.route('/')
def create() :
    return render_template('auth/login.html')


if __name__ == '__main__':
    app.run(debug=True)