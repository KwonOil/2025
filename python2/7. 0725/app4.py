from flask import Flask, make_response, render_template
from flask_cors import CORS
import json
import sqlite3

# DB 연결
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn

# 데이터 조회
def get_all_customers():

    conn = get_db_connection('python2/7. 0725/0725_customer.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()

    conn.close()
    return customers

# flask
app = Flask(__name__)
CORS(app)

# index
@app.route('/', methods=['GET'])
def index():
    customers = get_all_customers()
    columns = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]
    return render_template('test.html', customers=customers, columns=columns)

# api
@app.route('/api/<int:rn>', methods=['GET'])
def get_data(rn=1):
    customers = get_all_customers()
    columns = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]

    if rn == 1:
        customs = list(zip(*customers))
        result = {k:list(v) for k, v in zip(columns,customs)}
    elif rn == 2:
        result = [dict(zip(columns, customer)) for customer in customers]
    else:
        result = {customer[0]:dict(zip(columns[1:], customer[1:])) for customer in customers}

    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)