from flask import Flask, make_response
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

columns = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]
customer_tuples = [
    ("C001", "김철수", 35, "남성", 150000, "2024-03-15"),
    ("C002", "이영희", 28, "여성", 280000, "2024-03-14"),
    ("C003", "박민수", 42, "남성", 95000, "2024-03-13")
]

@app.route('/api', methods=['GET'])
def get_data():
    # result = [{'제품코드': 'P001',
    #             '제품명': '노트북',
    #             '카테고리': '전자기기',
    #             '재고수량': 50,
    #             '가격': 1200000,
    #             '입고일': '2024-02-01'}
    #         ]

    # 1 ~ 3 사이 정수를 무작위로
    rn =  random.randint(1, 3)

    if rn == 1:
        customs = list(zip(*customer_tuples))  
        result = {k:list(v) for k, v in zip(columns,customs)}
    elif rn == 2:
        result = [dict(zip(columns, customer)) for customer in customer_tuples]
    else:
        result = {customer[0]:dict(zip(columns[1:], customer[1:])) for customer in customer_tuples}

    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)