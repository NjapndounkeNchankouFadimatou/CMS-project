from flask import Blueprint, render_template ,request,url_for, session
from werkzeug.security import generate_password_hash
from db import dBase
user = Blueprint('user', __name__)
from model import Article, Category

@user.route('/all-articles')
def get_articles() :
    if 'name' in session :
        articles = Article.query.all()
        
        researched_article = request.args.get('research')
        result = []
    
        if researched_article :
            result = Article.query.join(Category).filter(or_(
                Article.titre.ilike(f"%{researched_article}%"),
                Category.nom.ilike(f"%{researched_article}%")
            )).all() #renvoie un article ou sa categorie dependament de si on trouve correspondance
            
            
        return render_template('user/index.html', articles=articles ,researched_articles=result )
    return render_template('auth/login.html')
               
            
"""
result = Article.query.filter(Article.title.ilike(f"%{researched_article}%")).all() 
#looks for all title that has in it name the research_artiicle

SELECT article.* 
FROM article 
JOIN category ON category.id = article.category_id 
WHERE article.title ILIKE '%mot%' 
   OR category.name ILIKE '%mot%';
"""
   
            
@user.route('/article/<content_name>' , methods=['GET'])
def content(content_name) :
    if 'name' in session :
        content_id = request.args.get('content_id')
        content = Article.query.filter_by(id=content_id).first()
        content_name = content.titre
        return render_template('user/art-details.html', content=content , content_name=content_name)
    
    return render_template('auth/login.html')
    
