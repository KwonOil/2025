from flask import Flask, make_response, request, render_template, redirect, url_for
from flask_cors import CORS
import json
import sqlite3
import matplotlib.pyplot as plt

# 맵플로립 백엔드(화면에 직접 표시하지 않고도 그래프를 파일로 저장)
import matplotlib
matplotlib.use('Agg')

# 맵플로립 한글설정{
import matplotlib.font_manager as fm
font_path = 'python2/0728_1/NanumSquareRoundR.ttf'
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rc('font', family=font_prop.get_name())
#}

app = Flask(__name__)
CORS(app)

def get_database():
    conn = sqlite3.connect('python2/0728_1/customer.db')
    return conn

conn = get_database()

cursor = conn.cursor()
cursor.execute('SELECT * FROM customer')
customer_tuples = cursor.fetchall()

columns = [desc[0] for desc in cursor.description]
conn.close()

def get_all_customers():
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()
    conn.close()
    return customers

def add_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
    conn = get_database()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO customer (id, name, age, gender, purchase_amount, purchase_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, name, age, gender, purchase_amount, purchase_date))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # ID가 이미 존재하는 경우 False 반환
    finally:
        conn.close()
    return True

def update_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE customer
        SET name=?, age=?, gender=?, purchase_amount=?, purchase_date=?
        WHERE id=?
    ''', (name, age, gender, purchase_amount, purchase_date, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customer WHERE id=?', (customer_id,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    customers = get_all_customers()
    columns = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]
    return render_template('index.html', customers=customers, columns=columns)

@app.route('/add', methods=['POST'])
def add():
    # [GET방식]
    #customer_id = request.args['customer_id']
    customer_id = request.form['customer_id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    purchase_amount = request.form['purchase_amount']
    purchase_date = request.form['purchase_date']

    if not add_customer(customer_id, name, age, gender, purchase_amount, purchase_date):
        return render_template('error.html', message="ID가 이미 존재합니다.")

    return redirect(url_for('index'))

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

@app.route('/delete/<customer_id>', methods=['POST'])
def delete(customer_id):
    delete_customer(customer_id)
    return redirect(url_for('index'))

@app.route('/api', methods=['GET'])
@app.route('/api/<int:data_id>', methods=['GET'])
def get_data(data_id=1):
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer')
    customer_tuples = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
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

@app.route('/statistics')
def statistics():
    conn = get_database()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT purchase_date, SUM(purchase_amount) as daily_sales
        FROM customer
        GROUP BY purchase_date
        ORDER BY purchase_date
    ''')
    sales_data = cursor.fetchall()
    
    dates = [row[0] for row in sales_data]
    sales = [row[1] for row in sales_data]
    
    total_sales = sum(sales)
    avg_sales = total_sales / len(sales) if sales else 0
    max_sales = max(sales) if sales else 0
    max_sales_date = dates[sales.index(max_sales)] if sales else '-'

    plt.figure(figsize=(12, 6))
    plt.bar(dates, sales, color='skyblue')
    plt.plot(dates, sales, marker='', color='blue', linewidth=.5, label='매출액 추세선')

    for i, v in enumerate(sales):
        plt.text(i, v + 1000, f'{v:,}원', ha='center', va='bottom', fontsize=10, color='blue', fontweight='bold', fontproperties=font_prop)
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(prop=font_prop)

    plt.title('일자별 매출 현황', pad=20, fontproperties=font_prop)
    plt.xlabel('구매 일자', fontproperties=font_prop)
    plt.ylabel('매출액(원)', fontproperties=font_prop)
    plt.xticks(rotation=0, fontsize=10)
    plt.grid(True)
    chart_path = "python2/0728_1/static/images/sales_chart.png"
    plt.savefig(chart_path, bbox_inches='tight', dpi=300)
    plt.close()

    # 성별 매출 통계
    cursor.execute('''
        SELECT gender, SUM(purchase_amount) as gender_sales, COUNT(*) as count
        FROM customer
        GROUP BY gender
    ''')
    gender_data = cursor.fetchall()
    
    # 연령대별 매출 통계 (10살 단위로 그룹화)
    cursor.execute('''
        SELECT (floor(age/10))*10 as age_group, SUM(purchase_amount) as age_sales, COUNT(*) as count
        FROM customer
        GROUP BY (floor(age/10))
        ORDER BY age_group
    ''')
    age_data = cursor.fetchall()

    # 성별 원형 차트
    plt.figure(figsize=(8, 8))
    gender_labels = [f"{row[0]}\n{row[1]:,}원\n({row[2]}명)" for row in gender_data]
    gender_sales = [row[1] for row in gender_data]
    plt.pie(gender_sales, labels=gender_labels, autopct='%1.1f%%', colors=['lightblue', 'pink'], textprops={'fontproperties': font_prop})
    plt.title('성별 매출 분포', fontproperties=font_prop)
    gender_chart_path = "python2/0728_1/static/images/gender_chart.png"
    plt.savefig(gender_chart_path, bbox_inches='tight', dpi=300)
    plt.close()

    # 연령대별 원형 차트
    plt.figure(figsize=(8, 8))
    age_labels = [f"{row[0]}대\n{row[1]:,}원\n({row[2]}명)" for row in age_data]
    age_sales = [row[1] for row in age_data]
    colors = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6']
    plt.pie(age_sales, labels=age_labels, autopct='%1.1f%%', colors=colors, textprops={'fontproperties': font_prop})
    plt.title('연령대별 매출 분포', fontproperties=font_prop)
    age_chart_path = "python2/0728_1/static/images/age_chart.png"
    plt.savefig(age_chart_path, bbox_inches='tight', dpi=300)
    plt.close()

    conn.close()

    return render_template('statistics.html', 
                         total_sales=total_sales,
                         avg_sales=round(avg_sales),
                         max_sales=max_sales,
                         max_sales_date=max_sales_date)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)