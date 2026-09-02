from db import dBase
from datetime import datetime

class User(dBase.Model) :
    id = dBase.Column(dBase.Integer, primary_key=True)
    name = dBase.Column(dBase.String(100) , nullable=False)
    email = dBase.Column(dBase.String(100) , nullable=False)
    password = dBase.Column(dBase.String(100) , nullable=False)
    role = dBase.Column(dBase.String(100) , default='admin')

    articles = dBase.relationship('Articles' , backref='auteur' ,lazy=True)

class Category(dBase.Model) :
    id = dBase.Column(dBase.Integer, primary_key=True)
    nom = dBase.Column(dBase.String(100), nullable=False)
    slug = dBase.Column(dBase.String(100), unique=True, nullable=False)

    articles = dBase.relationship('Article', backref='categorie', lazy=True)

class Article(dBase.Model) :
    id = dBase.Column(dBase.Integer, primary_key=True)
    titre = dBase.Column(dBase.String(200), nullable=False)
    slug = dBase.Column(dBase.String(200), unique=True, nullable=False)
    contenu = dBase.Column(dBase.Text, nullable=False)          # ⬅️ le texte principal, ici directement
    statut = dBase.Column(dBase.String(20), default='brouillon')
    template = dBase.Column(dBase.String(20) , default='image pricipal')
    date_creation = dBase.Column(dBase.DateTime, default=datetime.utcnow)

    id_auteur = dBase.Column(dBase.Integer, dBase.ForeignKey('user.id'), nullable=False)
    id_categorie = dBase.Column(dBase.Integer, dBase.ForeignKey('category.id'), nullable=True)
    medias = dBase.relationship('Contenu', backref='article', lazy=True, cascade='all, delete-orphan')

class Contenu(dBase.Model):
    id = dBase.Column(dBase.Integer, primary_key=True)
    type = dBase.Column(dBase.String(20), nullable=False)   # 'image', 'video', 'pdf'
    fichier = dBase.Column(dBase.String(255), nullable=False)   # chemin/nom du fichier uploadé
    ordre = dBase.Column(dBase.Integer, default=0)

    id_article = dBase.Column(dBase.Integer, dBase.ForeignKey('article.id'), nullable=False)