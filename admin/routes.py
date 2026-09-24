from flask import Blueprint, render_template ,request,url_for, session,redirect
from db import dBase
from model import Article, Category,User,Contenu

admin = Blueprint('admin', __name__)


@admin.route('/all-articles')
def get_articles() :
    if 'name' in session :
        articles = Article.query.all()
        
        researched_article = request.args.get('research')
        result = []
    
        if researched_article :
            result = Article.query.join(Category).filter(or_(
                Article.titre.ilike(f"%{researched_article}%"),
                Category.nom.ilike(f"%{researched_article}%")
            )).all() 
            
        return render_template('admin/index.html', articles=articles ,researched_articles=result )
    return render_template('auth/login.html')
    
@admin.route('/Dashboard')
def dashbord() :
    if 'name' in session :
        brouillon = Article.query.filter_by(statut='brouillon').order_by(Article.date_creation.desc()).all()
        publication = Article.query.filter_by(statut='publié').order_by(Article.date_creation.desc()).all()
        return render_template('admin/dashborad.html' , brouillon=brouillon ,publication=publication)
    return render_template('auth/login.html')

@admin.route('/Dashboard/<int:content_id>')
def dashboard_modification(content_id) :
    if 'name' in session :
        content_id = request.args.get('content_id')
        content = Article.query.get_or_404(content_id) 
        
     


def dashboard_delete(content_id) :
    if 'name' in session :
        content_id = request.args.get('content_id')
        content = Article.query.get_or_404(content_id) 
        
        dBase.session.delete(content)
        dBase.session.commit() 
        return redirect(url_for('admin.dashboard'))
        
def dashboard_change_status(content_id) :
        content_id = request.args.get('content_id')
        content = Article.query.filter_by(id=content_id).first()  
        
        if content.statut =='brouillon' :
            content.statut = 'publier'
        else :
            content.statut = 'brouillon'
    
@admin.route('/all-articles/<content_name>')
def content(content_name) :
    if 'name' in session :
        content_id = request.args.get('content_id')
        content = Article.query.filter_by(id=content_id).first()
        content_name = content.titre
        return render_template('admin/content.html', admin_content=content)
    
    return render_template('auth/login.html')

@admin.route('/Article_form' , methods=['GET','POST'])
def form_submission() :
    if 'name' in session :
        if request.method == 'POST' :
            title = request.form.get('title')
            texte = request.form.get('article_text')
            medias = request.form.get('medias')
            status = request.form.get('status')
            category = request.form.get('category')
            
            
            if category :
                new_category = Category.query.filter_by(nom=category).first()
                
            if not new_category :
                new_category = Category(nom=category)
                dBase.session.add(new_category)
                dBase.session.commit()
                
            article_category = new_category.id
           #author = session.get('name') #pour recuperer le nom de la personne ayant la session 
        
            user_id = session.get('id')
            #user = User.query.get(user_id)
            #author = user.name
            
            new_article = Article(titre=title , contenu=texte ,medias=medias , statut=status, art_categorie=article_category , user_id=user_id)
            dBase.session.add(new_article)
            dBase.session.commit()
                
            redirect(url_for('admin.dashboard'))
            
        return render_template('admin/article-form.html')
    return render_template('auth/login.html')   

    