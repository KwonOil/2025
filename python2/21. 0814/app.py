from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post_data():
    data = request.get_json(silent=True)
    search = request.args.get('search', '값 없음')

    if data:
        name = data.get('name')
        age = data.get('age')
        
        response_data = {
            'location': '삼성아카데미',
            'message': f"안녕하세요, {name}님! 와우 당신은 {age} 살이나 먹었네요~",
            'request': '학원컴퓨터',
            'received_data': data,
            'serch' : search
        }

        json_string = json.dumps(response_data, ensure_ascii=False)

        return Response(json_string, content_type="application/json; charset=utf-8"), 200
    else:
        return Response({'error': '잘못된 데이터입니다.'}, content_type="application/json; charset=utf-8"), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')