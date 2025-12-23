from flask import Flask
app = Flask(__name__)

BOOKS = {
    '979-11-6224-187-5': {
        'title': '혼자 공부하는 파이썬',
        'author': '윤인성',
        'publisher': '한빛미디어',
        'price': 22000,
        'stock': 15,
        'published_date': '2023-06-01'
    },
    '979-11-6224-028-1': {
        'title': '이것이 취업을 위한 코딩 테스트다 with 파이썬',
        'author': '나동빈',
        'publisher': '한빛미디어',
        'price': 34000,
        'stock': 8,
        'published_date': '2024-01-15'
    }
}

@app.route('/book/<isbn>')
def find_book(isbn):
    return '<b>Hello</b>, User!!! 하이~1'

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5000)