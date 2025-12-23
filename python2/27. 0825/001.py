## 라우팅
from flask import Flask

app = Flask(__name__)

@app.route('/')       # / 를 home()함수와 연결: 라우팅
@app.route('/home')   # /home 를 home()함수와 연결: 라우팅
def home():
    return 'Hello, World!!!'

# 리소스 변수는 함수의 인자값으로 넘어간다.
@app.route('/user')
def user():
    return '<b>Hello</b>, User!!! 하이~1'

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)