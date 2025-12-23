from flask import Flask, make_response, request, render_template, redirect, url_for
from flask_cors import CORS
import json
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('python2/7_2. 0725/0725_customer.db')
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

# 차트 데이터를 위한 API 라우트
@app.route('/api/chart/gender')
def get_gender_chart_data():
    # 데이터베이스에 연결합니다.
    conn = get_db_connection()
    cursor = conn.cursor()

    # '성별(gender)'로 그룹을 묶고, 각 그룹의 '구매금액(purchase_amount)'의 합계를 계산하는 SQL 쿼리를 실행합니다.
    # [('Female', 550000), ('Male', 800000)] 와 같은 형태로 결과를 반환합니다.
    cursor.execute('SELECT gender, SUM(purchase_amount) FROM customer GROUP BY gender')
    
    # 데이터베이스에서 모든 결과를 가져옵니다.
    data = cursor.fetchall()
    
    # 데이터베이스 연결을 닫습니다.
    conn.close()

    # Chart.js가 사용하기 좋은 형태로 데이터를 가공합니다.
    # labels 리스트와 data 리스트를 분리합니다.
    labels = [row[0] for row in data] # ['Female', 'Male']
    values = [row[1] for row in data] # [550000, 800000]

    # 최종적으로 JSON 형태로 응답을 생성합니다.
    # ensure_ascii=False 옵션은 한글이 깨지지 않게 합니다.
    chart_data = {
        'labels': labels,
        'values': values
    }
    response = make_response(json.dumps(chart_data, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


if __name__ == '__main__':
    app.run(debug=True)