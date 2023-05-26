from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.pal import Pal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/dashboard')
def dash():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    current_user = User.get_one({'id': user_id})
    all_users = User.get_all()
    return render_template("dash.html", current_user=current_user, users=all_users, user=current_user)

@app.route('/new/user', methods=['POST'])
def new_user():
    if not User.validate_register(request.form):
        return redirect('/')
    data = { 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/login')

@app.route('/signin', methods=['POST'])
def signin():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/edit/profile')
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    data = {'id': user_id}
    user = User.get_one(data)
    return render_template("ranking.html", user=user)

@app.route('/user/update', methods=['POST'])
def update_user():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    data = {
        'id': request.form['id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'ranking': request.form['ranking'],
        'about_me': request.form['about_me'],
    }
    if not User.validate_user_data(data):
        return redirect('/edit/profile')
    User.update_user_data(data)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/account/delete/<int:id>')
def delete(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    data = {"id": id}
    User.delete(data)
    return redirect('/')

@app.route('/view/<int:id>')
def view_user(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    session['selected_user_id'] = id
    selected_user = User.get_one({'id': id})
    return render_template("users.html", user=selected_user)