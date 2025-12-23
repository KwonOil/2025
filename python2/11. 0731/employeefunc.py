import json
import os
FILE_PATH = "python2\\11. 0731\\employees.json"
def clear_screen():
    """운영체제에 맞춰 콘솔 화면을 지우는 함수입니다."""
    # os.name을 통해 운영체제 확인 ('nt'는 Windows, 'posix'는 macOS/Linux)
    if os.name == 'nt':
        os.system('cls')  # Windows에서는 'cls' 명령어 실행
    else:
        os.system('clear') # macOS/Linux에서는 'clear' 명령어 실행
# --- 데이터 처리 함수 ---

def load_employees():
    """
    JSON 파일에서 직원 데이터를 불러오는 함수입니다.
    파일이 존재하지 않거나 비어있을 경우, 빈 리스트를 반환하여 오류를 방지합니다.
    """
    # 파일이 존재하는지 확인합니다.
    if not os.path.exists(FILE_PATH):
        return []  # 파일이 없으면 빈 리스트를 반환합니다.
    
    # 파일이 비어있는지 확인합니다.
    if os.path.getsize(FILE_PATH) == 0:
        return [] # 파일이 비어있으면 빈 리스트를 반환합니다.

    # 'with' 구문을 사용해 파일을 열고, 함수가 끝나면 자동으로 파일을 닫습니다.
    # 'r'은 읽기 모드, encoding='utf-8'은 한글 깨짐을 방지합니다.
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        try:
            # json.load() 함수를 사용해 파일의 JSON 데이터를 파이썬 리스트/딕셔너리로 변환합니다.
            return json.load(f)
        except json.JSONDecodeError:
            # 파일 내용이 올바른 JSON 형식이 아닐 경우, 빈 리스트를 반환합니다.
            return []

def save_employees(employees):
    """
    직원 데이터를 JSON 파일에 저장하는 함수입니다.
    """
    # 'w'는 쓰기 모드로, 파일이 이미 존재하면 내용을 덮어씁니다.
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # json.dump() 함수를 사용해 파이썬 객체(리스트)를 JSON 형식의 문자열로 변환하여 파일에 씁니다.
        # indent=4: JSON을 보기 좋게 4칸 들여쓰기로 저장합니다.
        # ensure_ascii=False: 한글이 유니코드(예: \u홍길동)가 아닌 원본 그대로 저장되도록 합니다.
        json.dump(employees, f, indent=4, ensure_ascii=False)

# --- 기능별 함수 ---

def add_employee(employees):
    """새로운 직원 정보를 입력받아 리스트에 추가합니다."""
    print("\n--- 직원 추가 ---")
    employee_id = input("직원 ID: ")

    # 이미 존재하는 ID인지 확인합니다.
    for emp in employees:
        if emp['id'] == employee_id:
            print("오류: 이미 존재하는 직원 ID입니다.")
            return

    # 새로운 직원 정보를 입력받습니다.
    name = input("이름: ")
    email = input("이메일: ")
    department = input("부서: ")

    # 입력받은 정보로 딕셔너리를 생성합니다.
    new_employee = {
        'id': employee_id,
        'name': name,
        'email': email,
        'department': department
    }

    # 생성된 딕셔너리를 전체 직원 리스트에 추가합니다.
    employees.append(new_employee)
    # 변경된 리스트를 파일에 저장합니다.
    save_employees(employees)
    print(f"'{name}' 직원의 정보가 성공적으로 추가되었습니다.")

def view_employees(employees):
    """모든 직원의 정보를 출력합니다."""
    print("\n--- 전체 직원 목록 ---")
    # 직원 데이터가 비어있는지 확인합니다.
    if not employees:
        print("등록된 직원이 없습니다.")
        return

    # 리스트의 각 직원에 대해 반복하면서 정보를 출력합니다.
    for emp in employees:
        print(f"ID: {emp['id']}, 이름: {emp['name']}, 이메일: {emp['email']}, 부서: {emp['department']}")

def update_employee(employees):
    """특정 직원의 정보를 수정합니다."""
    print("\n--- 직원 정보 수정 ---")
    employee_id = input("수정할 직원의 ID를 입력하세요: ")

    # 수정할 직원을 찾습니다.
    target_employee = None
    for emp in employees:
        if emp['id'] == employee_id:
            target_employee = emp
            break # 찾았으면 루프를 중단합니다.

    # 직원을 찾지 못한 경우
    if target_employee is None:
        print("오류: 해당 ID의 직원을 찾을 수 없습니다.")
        return

    # 새로운 정보를 입력받습니다. 입력을 안하고 엔터를 치면 기존 값을 유지합니다.
    print(f"(기존 이름: {target_employee['name']})")
    new_name = input("새 이름: ")
    if new_name: # 입력값이 있을 경우에만 변경
        target_employee['name'] = new_name

    print(f"(기존 이메일: {target_employee['email']})")
    new_email = input("새 이메일: ")
    if new_email:
        target_employee['email'] = new_email

    print(f"(기존 부서: {target_employee['department']})")
    new_department = input("새 부서: ")
    if new_department:
        target_employee['department'] = new_department

    # 변경된 내용을 파일에 저장합니다.
    save_employees(employees)
    print("직원 정보가 성공적으로 수정되었습니다.")

def delete_employee(employees):
    """특정 직원의 정보를 삭제합니다."""
    print("\n--- 직원 정보 삭제 ---")
    employee_id = input("삭제할 직원의 ID를 입력하세요: ")

    # 삭제할 직원을 찾습니다.
    target_employee = None
    for emp in employees:
        if emp['id'] == employee_id:
            target_employee = emp
            break

    # 직원을 찾지 못한 경우
    if target_employee is None:
        print("오류: 해당 ID의 직원을 찾을 수 없습니다.")
        return

    # 리스트에서 해당 직원을 제거합니다.
    employees.remove(target_employee)
    # 변경된 리스트를 파일에 저장합니다.
    save_employees(employees)
    print("직원 정보가 성공적으로 삭제되었습니다.")
