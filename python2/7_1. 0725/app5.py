from flask import Flask, make_response, request, render_template, redirect, url_for
from flask_cors import CORS
import json
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('python2/7_1. 0725/0725_customer.db')
    return conn

# 데이터베이스에서 모든 고객 정보를 가져오는 함수
def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()
    conn.close()
    return customers

# 고객 추가
def add_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO customer (id, name, age, gender, purchase_amount, purchase_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_id, name, age, gender, purchase_amount, purchase_date))
    conn.commit()
    conn.close()
    return True

# 고객 업데이트
def update_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE customer
        SET name=?, age=?, gender=?, purchase_amount=?, purchase_date=?
        WHERE id=?
    ''', (name, age, gender, purchase_amount, purchase_date, customer_id))
    conn.commit()
    conn.close()

# 고객 삭제
def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer WHERE id=?', (customer_id,))
    conn.commit()
    conn.close()

# 메인 페이지
@app.route('/', methods=['GET'])
def index():
    customers = get_all_customers()
    columns = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]
    return render_template('index.html', customers=customers, columns=columns)

# 고객 추가
@app.route('/add', methods=['POST'])
def add():
    customer_id = request.form['customer_id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    purchase_amount = request.form['purchase_amount']
    purchase_date = request.form['purchase_date']

    if not add_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
        return render_template('error.html', message="ID가 이미 존재합니다.")

    return redirect(url_for('index'))

# 고객 업데이트
@app.route('/update', methods=['POST'])
def update():
    customer_id = request.form['customer_id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    purchase_amount = request.form['purchase_amount']
    purchase_date = request.form['purchase_date']
    update_customer(customer_id, name, age, gender, purchase_amount, purchase_date)
    return redirect(url_for('index'))

# 고객 삭제
@app.route('/delete/<customer_id>', methods=['POST'])
def delete(customer_id):
    delete_customer(customer_id)
    return redirect(url_for('index'))

@app.route('/api', methods=['GET'])
@app.route('/api/<int:data_id>', methods=['GET'])
def get_data(data_id=1):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    customer_tuples = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # 컬럼명 리스트 추출
    conn.close()

    if data_id == 1:
        dim = list(zip(*customer_tuples))
        result = {k: list(v) for k, v in zip(columns, dim)}
    elif data_id == 2:
        result = [dict(zip(columns, customer)) for customer in customer_tuples]
    elif data_id == 3:
        result = {customer[0]:dict(zip(columns[1:], customer[1:])) for customer in customer_tuples}
    else:
        result = {'error': '잘못된 데이터 ID입니다.'}, 404

    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(debug=True)