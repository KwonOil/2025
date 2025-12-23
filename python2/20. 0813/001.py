### 장바구니 리스트

'''
1: 항목 추가
2: 항목 삭제
3: 목록 보기
4: 종료
원하는 작업을 선택하세요:
'''
## 항목 : 오이, 호박, 두부, 감자, 배추 ...
import os

class Product:
    def __init__(self):
        self.basket = []
        self.menu = True

    def show_menu():
        print("=== 메뉴 ===")
        print("1: 항목 추가")
        print("2: 항목 삭제")
        print("3: 목록 보기")
        print("4: 종료")

    # 해당 이름을 가진 상품이 있는지 확인
    def is_exist(self, name):
        for product in self.basket:
            if name in product['name']:
                return True
        return False

    # 이름과 가격을 입력받아 상품 추가, 상품이 이미 있으면 수량만 추가
    def add_product(self, name):
        if self.is_exist(name) == False:
            price = int(input("추가할 상품 가격을 입력하세요 : "))
            self.basket.append({ 'name' : name, 'price' : price, 'amount' : 1 })
        else:
            for product in self.basket:
                if name in product['name']:
                    product['amount'] += 1

    # 이름을 입력받아 수량 감소, 수량이 0이면 상품 삭제
    def del_product(self, name):
        for product in self.basket:
            if name in product['name']:
                product['amount'] -= 1
                if product['amount'] == 0:
                    self.basket.remove(product)

    # 상품 정보 출력, 상품이 없으면 없다고 출력
    def show_products(self):
        if not self.basket:
            print("상품이 없습니다.")
            return
        
        for product in self.basket:
            print(f"이름 : {product['name']}, 가격 : {product['price']}, 수량 : {product['amount']}")

    # 메인함수
    def main(self):
        while(True):
            if menu == True:
                os.system('cls')
                self.show_menu()
                choice = input("원하는 작업을 선택하세요 (1~4) : ")
            
            if choice == '1':
                os.system('cls')
                menu = False
                name = input("추가할 상품 이름을 입력하세요 (0 : 상위로 가기) : ")
                if(name == '0'):
                    menu = True
                    continue
                self.add_product(name)
                input(f"{name} 추가 완료되었습니다")
            elif choice == '2':
                os.system('cls')
                menu = False
                name = input("삭제할 상품 이름을 입력하세요 (0 : 상위로 가기) : ")
                if(name == '0'):
                    menu = True
                    continue
                self.del_product(name)
                input(f"{name} 삭제 완료되었습니다")
            elif choice == '3':
                os.system('cls')
                self.show_products()
                input("계속하려면 아무 키나 누르세요...")
            elif choice == '4':
                print("프로그램을 종료합니다...")
                break

a = Product()
a.main()