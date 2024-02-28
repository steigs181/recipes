from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/create/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
    "email": request.form['email'],
    "password" : pw_hash,
    "first_name" : request.form["first_name"],
    "last_name" : request.form['last_name']
    }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash("User already exists")
        return redirect('/')
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/recipes")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')