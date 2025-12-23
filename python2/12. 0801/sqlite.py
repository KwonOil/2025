import sqlite3

# 데이터베이스 서버(파일)에 접속
conn = sqlite3.connect('python2/12. 0801/userinfo.db')

# SQL을 사용하기 위한 객체 생성
cursor = conn.cursor()

# 테이블을 생성하는 SQL 쿼리 실행요청
def create_member():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS member (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()

# 테이블에 데이터를 추가하는 SQL 쿼리 실행요청
def add_member(username, name, email, password):
    cursor.execute('''
        INSERT INTO member (username, name, email, password)
        VALUES (?,?,?,?)
    ''',(username, name, email, password))
    conn.commit()

# 테이블에서 데이터를 삭제하는 SQL 쿼리 실행요청
def delete_member(id):
    cursor.execute('''
        DELETE FROM member WHERE id=?', (id)
    ''',(id))
    conn.commit()

# 테이블에서 데이터를 수정하는 SQL 쿼리 실행요청
def update_member(id, name, email, password):
    cursor.execute('''
        UPDATE member
        SET name=?, email=?, password=?
        WHERE id=?
    ''', (name, email, password, id))
    conn.commit()

# 테이블에서 데이터를 조회하는 SQL 쿼리 실행요청
def read_members():
    cursor.execute('SELECT * FROM member')
    return cursor.fetchall()

# create_member()
# add_member('홍씨', '홍길동', 'hong@a.com', '1234')
# add_member('이순신', '강철이', 'lee@a.com', '1234')
# update_member(1, "빛순이","hong@a.com","1234")

for row in read_members():
    print(row)

conn.close()