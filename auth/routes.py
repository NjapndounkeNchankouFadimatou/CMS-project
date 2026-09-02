from flask import Blueprint, render_template ,request,url_for, session
from werkzeug.security import generate_password_hash

auth= Blueprint('admin', __name__)

@auth.route('/register', methods=['POST', 'GET'])
def register() :
    if request.method == 'POST' :
        #data recuperation
        email = request.form.get('regis-email').strip()
        password = request.form.get('regis-password').strip()
        name = request.form.get('regis-name').strip()
        role = request.form.get('regis-role').strip()
        
        #data verification
        if not name :
            return render_template('auth/register.html' ,error ="Entrez votre nom")
        if not email :
            return render_template('auth/register.html' ,error ="Entrez un email valide")
        if not password or len(password) < 6 :
            return render_template('auth/register.html' ,error ="Entrez un mot de passe valide ")
 
        # hash du mot de passe
        hashed_password = generate_password_hash(password)
        
        #addition of data
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        
        
        #creation d'une sesssion
        dBase.session.add(new_user)
        dBase.session.commit()
        
        
        user_role = session['role']
        if new_user.role == 'admin' :
            return request.url(url_for('article-list'))
        else :
            return request.url(url_for('index'))
        
    return render_template('auth/register.html')
    
    
@auth.route('/login' , methods=['POST', 'GET'])
def login() :
    if request.method == 'POST' :
        email = request.form.get('login-email').strip()
        password = request.form.get('login-password').strip()

        #verifications of data
        if not email :
            return render_template('auth/login.html' ,error ="Entrez votre email")
        if not password or len(password) < 6:
            return render_template('auth/login.html' ,error ="Entrez un mot de passe valide ")
        
        if email != dBase_email :
            return render_template('register.html')
        

        
        
@auth.route('/logout')
def logout() :
    session.pop(user)