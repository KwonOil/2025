from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def encrypt_password(password):
    return generate_password_hash(password, method='sha256')

def verify_password(stored_password, input_password):
    return check_password_hash(stored_password, input_password)

password = "1234"
hashed_password = encrypt_password(password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_is_valid = verify_password(hashed_password, password)
        if user_is_valid:  
            session['username'] = username
            return redirect(url_for('home'))
        else:  
            return redirect(url_for('login_error'))
    return render_template('login.html')

@app.route('/login_error')
def login_error():
    return render_template('login_error.html')
