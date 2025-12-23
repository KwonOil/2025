import employeefunc as ef

def main():
    employees_data = ef.load_employees()

    while True:
        ef.clear_screen()
        print("\n===== 직원 관리 시스템 =====")
        print("1. 직원 추가")
        print("2. 직원 조회")
        print("3. 직원 수정")
        print("4. 직원 삭제")
        print("5. 종료")
        print("==========================")
        
        choice = input("메뉴를 선택하세요: ")

        if choice == '1':
            ef.add_employee(employees_data)
        elif choice == '2':
            ef.view_employees(employees_data)
        elif choice == '3':
            ef.update_employee(employees_data)
        elif choice == '4':
            ef.delete_employee(employees_data)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해주세요.")
        input()

if __name__ == "__main__":
    main()