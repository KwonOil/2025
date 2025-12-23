import mysql.connector

connection = mysql.connector.connect(
    host="192.168.0.192",      # MySQL 서버 주소
    user="root",           # 사용자명
    password="1234",   # 비밀번호
    database="mydb",        # 사용할 데이터베이스
    charset="utf8mb4",      # 문자 셋
    collation="utf8mb4_general_ci" # 문자 비교와 정렬 규칙
)
cursor = connection.cursor()

cursor.close()
connection.close()
