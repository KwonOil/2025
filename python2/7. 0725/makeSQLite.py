import sqlite3

field = ["고객ID", "이름", "나이", "성별", "구매금액", "구매날짜"]
customer_tuples = [
    ("C001", "김철수", 35, "남성", 150000, "2024-03-15"),
    ("C002", "이영희", 28, "여성", 280000, "2024-03-14"),
    ("C003", "박민수", 42, "남성", 95000, "2024-03-13")
]

conn = sqlite3.connect('python2/7. 0725/0725_customer.db')
cursor = conn.cursor()

# 테이블 생성 (없으면)
cursor.execute('''
CREATE TABLE IF NOT EXISTS customer (
    id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    purchase_amount INTEGER,
    purchase_date TEXT
)
''')

# 기존 데이터 삭제 (중복 입력 방지용)
cursor.execute('DELETE FROM customer')

# 데이터 삽입
cursor.executemany('''
INSERT INTO customer (id, name, age, gender, purchase_amount, purchase_date)
VALUES (?, ?, ?, ?, ?, ?)
''', customer_tuples)

conn.commit()
conn.close()