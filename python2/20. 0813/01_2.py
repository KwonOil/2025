### 장바구니 리스트
'''
1: 항목 추가
2: 항목 삭제
3: 목록 보기
4: 종료
원하는 작업을 선택하세요:
'''
## 항목: 오이, 호박, 두부, 감자, 배추 ...

import os
class Product:

    def __init__(self):
        self.items = []
        self.view_items = True

    def show_items(self):
        print("-" * 70)
        print(self.items)
        print("-" * 70)

    def main(self):
        while True:
            if self.view_items:
                os.system("cls")
                print("1: 항목 추가")
                print("2: 항목 삭제")
                print("3: 목록 보기")
                print("4: 종료")
                self.show_items()
                choice = input("원하는 작업을 선택하세요: ")
            
            if choice == '1':
                self.view_items = False
                os.system("cls")
                self.show_items()
                item = input("추가 항목 (0:상위로): ")
                
                if item=='0':
                    self.view_items = True
                    continue
                
                self.items.append(item)
                # print(f"{item}이(가) 추가되었습니다.")
                # input("아무 키나 누르세요...")
                
            elif choice == '2':
                self.view_items = False
                os.system("cls")
                self.show_items()
                item = input("삭제 항목 (0: 상위로): ")
                
                if item=='0':
                    self.view_items = True
                    continue

                if item in self.items:
                    self.items.remove(item)
                    #print(f"{item}이(가) 삭제되었습니다.")
                # else:
                #     print(f"{item}은(는) 목록에 없습니다.")
                # input("아무 키나 누르세요...")
                    
            elif choice == '3':
                print("현재 목록:", self.items)
                input("아무 키나 누르세요...")
                
            elif choice == '4':
                print("프로그램을 종료합니다.")
                break
                
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

a = Product()
a.main()
