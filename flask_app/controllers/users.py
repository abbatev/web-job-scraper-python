from flask_app import app, bcrypt 
from flask_app.models import user
from flask import render_template, session, request, redirect

#root
@app.route('/')
def sign_in():
    return render_template('sign_in.html',)

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html',)

#reg
@app.route('/registration/', methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/sign_up')
    hashed_password=bcrypt.generate_password_hash(request.form['password'])
    
    data={
    'first_name':request.form['first_name'],
    'last_name':request.form['last_name'],
    'email':request.form['email'],
    'password':hashed_password
    }

    one_user_id=user.User.create_user(data)
    session['logged_in_id']=one_user_id
    return redirect('/dashboard')

#login
@app.route('/login', methods=['POST'])
def login():
    one_user=user.User.validate_login(request.form)
    if not one_user:
        return redirect('/')
    session['logged_in_id']=one_user.id
    return redirect('/dashboard')

#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')