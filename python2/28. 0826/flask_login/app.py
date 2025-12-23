from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

#app = Flask(__name__)

#app.secret_key = 'your_secret_key'
app.secret_key = secrets.token_hex(16)
#app.config['SECRET_KEY'] = secrets.token_hex(16)

# MySQL 설정
db_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'database': 'samsungedu'
}

def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # cursor.execute("CREATE DATABASE IF NOT EXISTS samsungedu CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    # cursor.execute("USE samsungedu")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(100) NOT NULL
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_example_code():
    example_path = os.path.join(static_dir, 'examples', 'login_example.py')
    try:
        with open(example_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "예제 코드를 찾을 수 없습니다."

@app.route('/')
def home():
    init_db()
    if 'username' in session:
        example_code = get_example_code()
        return render_template('home.html', 
                             username=session['username'], 
                             name=session.get('name', ''),
                             example_code=example_code)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        #[0] id         int(11)      NOT NULL
        #[1] username   varchar(50)  NOT NULL
        #[2] password   varchar(255) NOT NULL
        #[3] name       varchar(50)  NOT NULL
        #[4] phone      varchar(20)  NOT NULL
        #[5] email      varchar(100) NOT NULL

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['name'] = user[3]  
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_error'))
    return render_template('login.html')

@app.route('/login_error')
def login_error():
    return render_template('login_error.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users 
                (username, password, name, phone, email) 
                VALUES (%s, %s, %s, %s, %s)
            """, (username, hashed_password, name, phone, email))
            conn.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"오류가 발생했습니다: {err}"
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port=5005)