# db.py
# 목적: MySQL 연결을 생성하는 헬퍼 모듈
# - PyMySQL을 사용하여 커넥션을 만드는 함수 제공
# - with 문 사용을 권장(사용 후 자동 close)
# - DictCursor로 결과를 dict 형태로 받기 편하도록 설정

import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# .env 파일 로드 (없어도 동작은 하나, 개발 편의를 위해 지원)
load_dotenv()

def get_connection():
    """
    MySQL DB 커넥션을 생성하여 반환합니다.
    - autocommit=False로 두고, 트랜잭션은 명시 커밋/롤백합니다.
    - DictCursor를 사용하여 행을 dict로 받습니다.
    """
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", ""),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )
    return conn
