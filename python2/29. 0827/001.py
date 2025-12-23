import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="192.168.0.181",      # MySQL 서버 주소
    user="root",           # 사용자명
    password="1234",   # 비밀번호
    database="mydb"        # 사용할 데이터베이스
)
cursor = conn.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS score (
    idx INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    dept VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    p_score TINYINT(4) NULL DEFAULT '0',
    m_score TINYINT(4) NULL DEFAULT '0',
    f_score TINYINT(4) NULL DEFAULT '0',
    h_score TINYINT(4) NULL DEFAULT '0',
    PRIMARY KEY (idx)
)'''
)
df = pd.read_excel("python2/29. 0827/file.xlsx", skiprows=1)
# for i, row in df.iterrows():
#     cursor.execute('''
#     insert into score(name, dept, p_score, m_score, f_score, h_score) values(%s, %s, %s, %s, %s, %s)
#     ''', tuple(row)[1:])
#     print(tuple(row)[1:])
for row in df.itertuples(index=False, name=None):
    cursor.execute('''
    insert into score(name, dept, p_score, m_score, f_score, h_score) values(%s, %s, %s, %s, %s, %s)
    ''', row[1:])
    print(row[1:])

conn.commit()
cursor.close()
conn.close()