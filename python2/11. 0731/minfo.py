import os
import csv
import json

def write_file4csv(filename):
    name = input("이름을 입력하세요")
    email = input("이메일을 입력하세요")
    
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, "w", encoding = 'utf-8') as f:
            f.write("이름, 이메일\n")

    with open(filename, "a+", encoding = 'utf-8') as f:
        if ',' in name: name = f'"{name}"'
        if ',' in email: email = f'"{email}"'
        f.write(f'''{name}, {email}\n''')

def read_file4csv(filename):
    with open(filename, "r", encoding = 'utf-8') as f:
        content = f.read()
    return content

def create_json(filename):
    header = ['이름','나이','전공']
    values = [input("이름을 입력하세요"), int(input("나이를 입력하세요")), input("전공을 입력하세요")]

    student = {h : values[i] for i, h in enumerate(header)}

    students = []
    students.append(student)

    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent = 4)

def read_json(filename):
    with open('students.json', 'r', encoding = 'utf-8') as f:
        s = json.load(f)
    return s

def update_json_file(filename):
    name = input("추가할 학생 이름을 입력하세요: ")
    age = int(input("학생 나이를 입력하세요: "))
    major = input("전공을 입력하세요: ")
    
    try:
        with open(filename, "r", encoding='utf-8') as file:
            students = json.load(file)
    except FileNotFoundError:
        students = []

    students.append({"name": name, "age": age, "major": major})

    with open(filename, "w", encoding='utf-8') as file:
        json.dump(students, file, ensure_ascii=False, indent=4)

def search_student():
    name_to_search = input("검색할 학생 이름: ")
    
    try:
        with open("students.json", "r", encoding="utf-8") as f:
            students = json.load(f)
            found = False
            
            for student in students:
                if student["이름"] == name_to_search:
                    print("학생 정보:", student)
                    found = True
            
            if not found:
                print("해당 학생을 찾을 수 없습니다.")
    except FileNotFoundError:
        print("학생 정보 파일이 없습니다.")

def json_to_csv(jsonfilename,csvfilename):
    try:
        with open(jsonfilename, 'r', encoding = 'utf-8') as f:
            students = json.load(f)

            with open(csvfilename, 'w', encoding = 'utf-8', newline='') as f:
                wr = csv.writer(f)
                wr.writerow(students[0].keys())
                wr.writerows([student.values() for student in students])
            print("CSV 파일이 성공적으로 생성되었습니다.")
    except FileNotFoundError:
            print("학생 정보 파일이 없습니다.")

def read_students(filename, opt=1):
    
    if opt==1:
        data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            #header = f.readline().strip().split(",")
            header = next(f).strip().split(',')  
            for line in f:
                values = line.strip().split(',')
                for k, v in zip(header, values):
                    if k not in data:
                        data[k] = []
                    data[k].append(int(v) if v.isdigit() else v)
    elif opt==2:
        data = []
        with open(filename, 'r', encoding='utf-8') as f:
            header = next(f).strip().split(',')
            for line in f:
                values = line.strip().split(',')
                student = {k: (int(v) if v.isdigit() else v) for k, v in zip(header, values)}
                data.append(student)
    return data