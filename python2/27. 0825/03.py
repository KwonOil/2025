from flask import Flask, render_template

app = Flask(__name__)

sample_params = {
    'search': '노트북',
    'min_price': '1000000',
    'max_price': '2000000',
    'sort': 'price_desc'
}

@app.route('/')
@app.route('/products')
def product_list():
    return render_template('products.html', params3 = sample_params)

if __name__ == '__main__':
    app.run(debug=True)