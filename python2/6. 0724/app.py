from flask import Flask, make_response
from flask_cors import CORS
import json

# data
columns = ["제품코드","제품명","카테고리","재고수량","가격","입고일"]
inventory_tuple = [
    ("P001", "노트북", "전자기기", 50, 1200000, "2024-02-01"),
    ("P002", "스마트폰", "전자기기", 100, 850000, "2024-02-15"),
    ("P003", "이어폰", "액세서리", 200, 180000, "2024-03-01")
]
def toJSON(keys, tuples):
    return [ dict(zip(keys,i)) for i in inventory_tuple]
data = toJSON(columns,inventory_tuple)

# flask
app = Flask('__name__')
CORS(app)

@app.route('/api',methods=['GET'])
def get_data():
    response = make_response(json.dumps(data, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)