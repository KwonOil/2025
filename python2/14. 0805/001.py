from datetime import datetime
import os
import mysql.connector

# DB 설정과 연결
config = {
    'user': 'hong',
    'password': '1234',
    'host': 'localhost',
    'database': 'db0804',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}
conn = mysql.connector.connect(**config)

cursor = conn.cursor()

def clear_screen():
    os.system('cls') if os.name == 'nt' else os.system('clear')

# DB에 일정 추가
def add_db(event_name, event_date):
    cursor.execute('''
        INSERT INTO events (event_name, event_date)
        VALUES (%s, %s)
    ''', (event_name, event_date))
    conn.commit()

# DB에서 일정 목록 전부 가져오기
def read_all():
    cursor.execute('SELECT event_name, event_date FROM events')
    return cursor.fetchall()

# DB에서 일정 목록 수정하기
def update_event(id):
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
    cursor.execute('DELETE FROM events WHERE id = %s', (id,))
    conn.commit()

# 일정 추가하기
def add_event(name, edate):
    add_db(name, edate)

# 모든 일정 보기
def show_events():
    e = read_all()
    if not e:
        print("일정이 없습니다.")
        return

    print("\n[모든 일정]")
    for event_name, event_date in e:
        print(f"- {event_name} : {event_date.strftime('%Y년 %m월 %d일 %H시 %M분')}")

# 남은 일정 보기
def remain_events():
    e = read_all()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    if not e:
        print("일정이 없습니다.")
        return

    print("\n[남은 일정]")
    for event_name, event_date in e:
        if now <= event_date.strftime('%Y-%m-%d %H:%M'):
            print(f"- {event_name} : {event_date.strftime('%Y년 %m월 %d일 %H시 %M분')}")

def show_menu():
    print("\n일정 관리 프로그램")
    print("1. 일정 추가")
    print("2. 모든 일정 보기")
    print("3. 남은 일정 보기")
    print("4. 일정 삭제하기")
    print("5. 일정 수정하기")
    print("6. 종료")

def main():
    while(True):
        clear_screen()
        show_menu()
        choice = input("원하는 작업을 선택하세요(1 ~ 6) :")
        if choice == '6':
            break
        elif choice == '1':
            name = input("일정 제목을 입력하세요 :")
            edate = input("일정 날짜를 입력하세요(YYYY-MM-DD HH:MM) :")
            add_event(name, edate)
        elif choice == '2':
            show_events()
        elif choice == '3':
            remain_events()
        elif choice == '4':
            delete_member(input("삭제할 id를 입력하세요 : "))
        elif choice == '5':
            update_event(input("수정할 id를 입력하세요 : "))
        input("계속하려면 아무 키나 누르세요...")
    cursor.close()

if __name__ == '__main__':
    main()