from flask import Blueprint, request, redirect, render_template, session, flash
import flask
from models.user import get_user_by_email
import bcrypt


session_controller = Blueprint("session_controller", __name__, template_folder="../templates/user")

@session_controller.route('/login')
def loginpage():

    return render_template('/user/login.html')

@session_controller.route('/login/create', methods=["POST"])
def login():

    email = request.form.get('email')
    user = get_user_by_email(email)
    password = request.form.get('password')
    hashed_password = user['password']
    
    if user and bcrypt.checkpw(password.encode(), hashed_password.encode()):
        #update session
        session['user_id'] = user['id']
        session['user_name'] = user['first_name']
        flash(f'Hi {user[1]}, Welcome Back!')
        return redirect('/home')
    else:
         #redirect  
        flash(f'Incorrect Username or Password. Please Try Again.')
        return redirect('/login?error=Incorrect')  


@session_controller.route('/sessions/delete', methods=["GET", "POST"])
def logout():
    session['user_id'] = None
    session['user_name'] = None
    return redirect('/')