from flask import Blueprint, render_template ,request,url_for, session,redirect
from db import dBase
from model import Article, Category,User,Contenu

admin = Blueprint('admin', __name__)

@admin.route('/all-articles')
def article_list() :
    if 'name' in session :
        brouillon = Article.query.filter_by(statut=brouillon).order_by(date_creation=desc)
        publication = Article.query.filter_by(statut=publication).order_by(date_creation=desc)
        return render_template('admin/articles-list.html' , brouillon=brouillon ,publication=publication)
    return render_template('auth/login.html')

@admin.route('/all-articles/<content_name>')
def content(content_name) :
    if 'name' in session :
        content_id = request.args.get('content_id')
        content = Article.query.filter_by(id=content_id).first()
        content_name = content.titre
        return render_template('admin/content.html', admin_content=content)
    
    return render_template('auth/login.html')

@admin.route('/Dashboard' , methods=['GET','POST'])
def dashboard() :
    if 'name' in session :
        if request.method == 'POST' :
            title = request.form.get('title')
            category = request.form.get('category')
            texte = request.form.get('article_text')
            medias = request.form.get('medias')
            status = request.form.get('status')
        
            new_article = Article(titre=title , contenu=texte ,medias=medias , statut=status)
            dBase.session.add(new_article)
            dBase.session.commit()
            
            if not category in Category.query.all() :
                new_category = Category(nom=category)
                dBase.session.add(new_category)
                dBase.session.commit()
                
            redirect(url_for('admin.article_list'))
            
        return render_template('admin/article-form.html')
    return render_template('auth/login.html')   

def modifcation() :
    