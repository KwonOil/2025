import mysql.connector

# DB 설정과 연결
def get_db():
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'db0804',
        'port': 3306,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci'
    }
    
    return mysql.connector.connect(**config)

# DB에 일정 추가
def add_db(event_name, event_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (event_name, event_date)
        VALUES (%s, %s)
    ''', (event_name, event_date))
    conn.commit()

# DB에서 일정 목록 전부 가져오기
def read_all():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT event_name, event_date FROM events')
    return cursor.fetchall()

# DB에서 일정 목록 수정하기
def update_event(id):
    conn = get_db()
    cursor = conn.cursor()
    name = input("수정할 일정 제목을 입력하세요 : ")
    date = input("수정할 일정 날짜를 입력하세요 : ")
    cursor.execute('''
        UPDATE events
        SET event_name = %s, event_date = %s
        WHERE id = %s
    ''', (name, date, id))
    conn.commit()

# DB에서 일정 삭제하기
def delete_member(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = %s', (id,))
    conn.commit()