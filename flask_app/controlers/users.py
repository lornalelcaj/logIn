from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if id not in session:
        return redirect('/logIn')

@app.route('/logIn')
def logIn():
    return render_template("login.html")

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        flash("Email and pass required", 'signUp')
        return redirect(request.referrer)

    if User.getUserByEmail(request.form):
        flash("This email already exists", 'emailRegister')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.addUser(data)
    return redirect(request.referrer)

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Required Email", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("Email doenst exist", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Wrong password!", 'passwordLogin')
        return redirect(request.referrer)
    
    session['user_id'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id' : session['user_id']
        }
        print(data)
        user = User.getUserById(data)
        return render_template("dashboard.html", loggedUser = user  )
    return redirect('/logout')


@app.route('/logout')
def destroy():
    session.clear()
    return redirect('/')