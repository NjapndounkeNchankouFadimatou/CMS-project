from flask import Blueprint, render_template ,request,url_for, session, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from db import dBase
from model import User
from user.routes_user import user
from datetime import timedelta

auth= Blueprint('auth', __name__)
auth.permanent_session_lifetime = timedelta(days=7)


@auth.route('/register', methods=['POST', 'GET'])
def register() :
    if request.method == 'POST' :
        #data recuperation
        email = request.form.get('regis-email').strip()
        password = request.form.get('regis-password').strip()
        name = request.form.get('regis-name').strip()
        role = request.form.get('regis-role').strip()
        
        existingUser = User.query.filter_by(email=email).first()
        
        #data validation
        if not name :
            return render_template('auth/register.html' ,error ="Entrez votre nom")
        
        if not email  or existingUser:
            return render_template('auth/register.html' ,error ="Entrez un email valide ou logger vous")
        if not password or len(password) < 6 :
            return render_template('auth/register.html' ,error ="Entrez un mot de passe valide ")
 
        #password hash
        hashed_password = generate_password_hash(password)
        
        #addition of data
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        dBase.session.add(new_user)
        dBase.session.commit()

        #creation of user session
        session.permanent = True
        session['name'] = name
        session['role'] = role
        
        if session.get('role') == 'admin':
            return redirect(url_for('user.get_articles'))
        else :
            return redirect(url_for('user.get_articles'))
            
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
        
        existingUser = User.query.filter_by(email=email).first()
        if existingUser is None :
            print("No user found with this email.") #add a flash message          
            return render_template('auth/login.html', error='Enter a valide email or password')
            
        checkPassword = check_password_hash(existingUser.password, password)
        if not checkPassword :
            return render_template('auth/login.html', error='Mot de passe incorrect')
        
        if 'name' in session:
            if session.get('role') == 'admin':
                return redirect(url_for('user.article-form'))
            else :
                return redirect(url_for('user.get_articles'))
        
    return render_template('auth/login.html')
        

@auth.route('/logout')
def logout() :
    session.clear()
    render_template('auth/register.html')