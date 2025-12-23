from flask import Flask, render_template
app = Flask(__name__)

# templates/


@app.route('/')
def index():
    # return "<h1>텍스트</h1>"
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/product')
def product():
    # 제품 데이터 정의
    products = [
        {
            'name': '제품 A',
            'price': 10000,
            'description': '이 제품은 매우 훌륭한 제품입니다. 구매하시면 만족하실 것입니다.'
        },
        {
            'name': '제품 B',
            'price': 35000,
            'description': '이 제품은 특별합니다. 품질이 탁월하며 사용하기 편합니다.'
        },
        {
            'name': '제품 C',
            'price': 47000,
            'description': '이 제품은 다양한 기능을 제공하며 합리적인 가격으로 구입하실 수 있습니다.'
        }
    ]
    return render_template('product_list.html', products=products)

@app.route('/greeting/<name>')
def greeting(name):
    return render_template('greeting.html', template_variable=name)

@app.route('/dictionary')
def dictionary():
    template_dict = {
        'apple': 1,
        'banana': 2,
        'cherry': 3,
        'date': 4,
        'elderberry': 5,
        'fig': 6
    }
    return render_template('dictionary.html', template_dict=template_dict)

if __name__ == '__main__':
    app.run(debug=True)