from flask import Blueprint, render_template ,request,url_for, session
from werkzeug.security import generate_password_hash
from db import dBase
from model import Article, User, Category,Contenu


user = Blueprint('user', __name__)

@user.route('/all-articles')
def get_articles() :
    articles = Article.query.all()
    return render_template('user/index.html', Articles=articles)
    

@user.route('/article/<int:id>')
def content(id) :
    content_id = id
    research = Contenu.query.filter_by(content_id)
    return render_template('user/art-details.html', research=research)
    
