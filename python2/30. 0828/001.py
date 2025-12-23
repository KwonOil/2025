import mysql.connector
import json

connection = mysql.connector.connect(
    host="192.168.0.181",      # MySQL 서버 주소
    user="root",           # 사용자명
    password="1234",   # 비밀번호
    database="mydb",        # 사용할 데이터베이스
    charset="utf8mb4",      # 문자 셋
    collation="utf8mb4_general_ci" # 문자 비교와 정렬 규칙
)
# cursor = connection.cursor(dictionary = True)

# sql = '''SELECT *, (p_score+m_score+f_score+h_score) AS total FROM score 
# WHERE dept='컴퓨터공학과' AND (p_score+m_score+f_score+h_score) >= 85
# ORDER BY total DESC
# '''

sql = '''
SELECT dept, `name`, (p_score+m_score+f_score+h_score) AS score,
CASE
    WHEN (p_score+m_score+f_score+h_score) >= 90 THEN 'A'
    WHEN (p_score+m_score+f_score+h_score) >= 80 THEN 'B'
    WHEN (p_score+m_score+f_score+h_score) >= 70 THEN 'C'
    WHEN (p_score+m_score+f_score+h_score) >= 60 THEN 'D'
    ELSE 'F'
END AS grade
FROM score
WHERE dept = '컴퓨터공학과'
ORDER BY FIELD (grade, 'F','D','C','B','A')
'''
# cursor.execute(sql)

# data = cursor.fetchall()

# cursor.close()
# connection.close()

# print(data)
# print(json.dumps(data, ensure_ascii=False, indent=2)) # json.dumps(data)

cursor = connection.cursor()
# 테이블 생성쿼리 가져오기
cursor.execute("SHOW CREATE TABLE score")

# 결과 가져오기
result = cursor.fetchone()

# 결과 출력
if result:
    print("테이블명:", result[0])
    print("테이블 생성 구문:")
    print(result[1])
else:
    print("테이블이 존재하지 않아요.")

cursor.close()
connection.close()