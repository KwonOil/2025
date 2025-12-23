'''
===== 가계부 =====
1: 지출 입력
2: 지출 삭제
3: 지출 목록 보기
4: 총 지출 확인
0: 종료
원하는 작업을 선택하세요 1

[1]
날짜를 입력하세요 (예: 11-19): 11
지출 항목을 입력하세요: 커피
금액을 입력하세요: 5000
지출이 기록되었습니다.

[2]
날짜    항목    금액
------------------------
11    커피    5,000원
15    점심    9,000원

[3]
총 지출: 14,000원
'''
import mysql.connector
import os

class DB:
    def __init__(self, database = 'expenses_db'):
        self.database = database
        self.config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': database,
        'port': 3306,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci'
        }
        self.create_datebase()

    # 데이터베이스 커넥션을 반환
    def get_db(self):
        conn = mysql.connector.connect(**self.config)
        return conn

    # 데이터베이스 생성
    def create_datebase(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE DATABASE IF NOT EXISTS {self.database} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
            ''')
            self.config['database'] = self.database
            conn.commit()

    # 테이블 생성
    def create_tables(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cash (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    date INT NOT NULL,
                    item VARCHAR(100) NOT NULL,
                    expend INT NOT NULL
                )
            ''')
            conn.commit()

    # 지출 목록 보기
    def get_expend(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(''' SELECT date, item, expend FROM cash ''')
            return cursor.fetchall()

    # 지출 입력
    def add_expend(self, name, date, item, expend):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cash (name, date, item, expend)
                VALUES (%s, %s, %s, %s)
            ''', (name, date, item, expend))
            conn.commit()

    # 지출 삭제
    def del_expend(self, date, item):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM cash WHERE date = %s AND item = %s
            ''', (date, item))
            conn.commit()

    # 총 지출
    def total_expend(self):
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT SUM(expend) FROM cash
            ''')
            return cursor.fetchone()[0] or 0

class ExpenseTracker(DB):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    # 메뉴 출력
    def show_menu(self):
        print(f'===== {self.name} 가계부 =====')
        print('1: 지출 입력')
        print('2: 지출 삭제')
        print('3: 지출 목록 보기')
        print('4: 총 지출 확인')
        print('0: 종료')

    # 지출 입력
    def add_expend(self):
        date = input('날짜를 입력하세요 (예: 11-19): ')
        item = input('지출 항목을 입력하세요: ')
        expend = int(input('금액을 입력하세요: '))
        return super().add_expend(self.name, date, item, expend)
    
    # 지출 삭제
    def del_expend(self):
        date = input('날짜을 입력하시오: ')
        item = input('지출 항목을 입력하시오: ')
        return super().del_expend(date, item)
    
    # 지출 목록 보기
    def show_expend(self):
        print(f'날짜\t\t항목\t\t금액')
        print('----------------------------------------')
        for row in super().get_expend():
            print(f'{row[0]}\t\t{row[1]}\t\t{row[2]:,}원')

    # main
    def main(self):
        self.create_tables()
        while True:
            os.system('cls')
            self.show_menu()
            choice = input('원하는 작업을 선택하세요 : ')
            if choice == '1':
                self.add_expend()
                print('지출이 기록되었습니다.')
            elif choice == '2':
                self.del_expend()
                print('지출내역이 삭제되었습니다.')
            elif choice == '3':
                self.show_expend()
            elif choice == '4':
                print(f'총 지출: {self.total_expend():,}원')
            elif choice == '0':
                break
            else:
                print('잘못된 입력입니다. 올바른 숫자를 입력해 주세요')
            input('계속하려면 아무 키나 누르세요...')

if __name__ == '__main__':
    tracker = ExpenseTracker('권오일')
    tracker.main()