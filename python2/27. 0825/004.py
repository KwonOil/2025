from flask import Flask
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# 샘플 데이터
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

BUS_STOPS = {
    '12345': {
        'name': '강남역 2번출구',
        'routes': ['140', '147', '462'],
        'location': '서울특별시 강남구 강남대로 지하 396'
    },
    '12346': {
        'name': '역삼역 3번출구',
        'routes': ['147', '462', '341'],
        'location': '서울특별시 강남구 강남대로 지하 416'
    }
}

STUDENTS = {
    '20240001': {
        'name': '김철수',
        'grade': 2,
        'class': 3,
        'scores': {
            'korean': 92,
            'math': 88,
            'english': 90,
            'science': 85
        }
    }
}

RESTAURANTS = {
    'korean-bbq-01': {
        'name': '맛있는 고기집',
        'address': '서울시 강남구 역삼동 123-45',
        'tel': '02-555-1234',
        'reservations': {
            'R12345': {
                'date': '2024-12-25',
                'time': '19:00',
                'people': 4,
                'name': '김예약'
            }
        }
    }
}

WORKOUTS = {
    'kim123': {
        'running': [
            {
                'date': '2024-12-20',
                'duration': 45,
                'distance': 5.2,
                'calories': 400
            }
        ]
    }
}

# 1. 도서 검색 API
@app.route('/book/<isbn>')
def find_book(isbn):
    book = BOOKS.get(isbn)
    if not book:
        return '죄송합니다. 해당 도서를 찾을 수 없습니다.'

    return f"""
[도서 정보]
제목: {book['title']}
저자: {book['author']}
출판사: {book['publisher']}
가격: {book['price']:,}원
재고: {book['stock']}권
출판일: {book['published_date']}
"""

# 2. 버스 도착 정보 API
@app.route('/bus/<bus_number>/stop/<stop_id>')
def bus_arrival(bus_number, stop_id):
    stop = BUS_STOPS.get(stop_id)
    if not stop:
        return '죄송합니다. 해당 정류장을 찾을 수 없습니다.'

    if bus_number not in stop['routes']:
        return '해당 버스가 이 정류장을 지나지 않습니다.'

    arrival1 = random.randint(1, 15)
    arrival2 = random.randint(16, 30)

    return f"""
[버스 도착 정보]
정류장: {stop['name']}<br>
위치: {stop['location']}<br>
노선번호: {bus_number}번<br>
첫 번째 버스: {arrival1}분 후<br>
두 번째 버스: {arrival2}분 후<br>
현재 시각: {datetime.now().strftime('%H:%M:%S')}
"""

# 3. 학생 성적 조회 API
@app.route('/grade/<student_id>/<subject>')
def check_grade(student_id, subject):
    student = STUDENTS.get(student_id)
    if not student:
        return '죄송합니다. 해당 학생을 찾을 수 없습니다.'

    score = student['scores'].get(subject)
    if score is None:
        return '죄송합니다. 해당 과목을 찾을 수 없습니다.'

    return f"""
[성적 정보]
학생: {student['name']}<br>
학년-반: {student['grade']}학년 {student['class']}반<br>
과목: {subject}<br>
점수: {score}점
"""

# 4. 식당 예약 확인 API
@app.route('/reservation/<restaurant_id>/<reservation_id>')
def check_reservation(restaurant_id, reservation_id):
    restaurant = RESTAURANTS.get(restaurant_id)
    if not restaurant:
        return '죄송합니다. 해당 식당을 찾을 수 없습니다.'

    reservation = restaurant['reservations'].get(reservation_id)
    if not reservation:
        return '죄송합니다. 해당 예약을 찾을 수 없습니다.'

    return f"""
[예약 확인]
식당명: {restaurant['name']}
주소: {restaurant['address']}
연락처: {restaurant['tel']}
예약자: {reservation['name']}
예약 날짜: {reservation['date']}
예약 시간: {reservation['time']}
예약 인원: {reservation['people']}명
"""


# 5. 운동 기록 조회 API
@app.route('/workout/<username>/<workout_type>/<date>')
def workout_log(username, workout_type, date):
    user_workouts = WORKOUTS.get(username)
    if not user_workouts:
        return '죄송합니다. 해당 사용자를 찾을 수 없습니다.'

    workout_list = user_workouts.get(workout_type, [])
    workout = next((w for w in workout_list if w['date'] == date), None)

    if not workout:
        return '죄송합니다. 해당 날짜의 운동 기록을 찾을 수 없습니다.'

    return f"""
[운동 기록]
사용자: {username}<br>
운동 종류: {workout_type}<br>
날짜: {workout['date']}<br>
운동 시간: {workout['duration']}분<br>
이동 거리: {workout['distance']}km<br>
소모 칼로리: {workout['calories']}kcal
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)