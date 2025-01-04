import random #random 모듈 불러오기
import time #time 모듈 불러오기
#random.seed(213)

class Station: 
    # 인스턴스 변수
    def __init__(self): #변수 선언
        self.day = 1 # 현재까지의 총 영업일(Day XX)을 표시하는 변수
        self.rating = 0 # 주유소의 평판
        self.money = 1000.00 # 보유 금액
        self.Diesel = 100 # 주유소가 가지고 있는 디젤의 양
        self.Gasoline = 100 # 주유소가 가지고 있는 가솔린의 양
        self.Diesel_selling_price=10.00 # 처음 디젤의 판매가격
        self.Gasoline_selling_price=15.00 # 처음 가솔린의 판매가격 
        self.rs={'for_free': [3, "Driver: I'm blessed to have all of these. Thanks!"],
'let_go': [-1, "Owner: Currently, we are not available for that.\nDriver: Well, see you then!"],
'good_job': [1, "Driver: Thanks a lot!"],
'wrong_fuel': [-5, "System: This is not the right fuel type!"],
'overflow': [-3, "Driver: Hey, it overflows! Stop there!"],
'different': [-1, "Driver: Well, not the exact amount, but thanks anyway!"],
'not_enough': [-1, "System: There is not enough fuel in the tank!"],
} # 주유시 표출되는 메시지와 평판 변화를 담은 딕셔너리
        self.today_num = 0 # 오늘의 고객 수
        self.total_num = 0 # 전체 고객 수
        self.customer = None # 현재 응대 중인 고객. 없는 경우 None
        self.del_rating = 0 #평판의 변화량
        self.init_oiltype= 'Gasoline' # 주유방식의 연료종류 초깃값
        self.init_oil= 10 # 주유방식의 연료량 초깃값
        

    # 메서드
    def state_update(self): # 고객 응대에 따라 평판을 업데이트하는 함수
        print("Rating: %d -> %d" %(self.rating, self.rating+self.del_rating))
        self.rating+=self.del_rating
        

    def refill(self): # 상점으로부터 기름을 구매하는 함수
        ans_refill = input('''\nWhich one do you want to refill?
0. Diesel
1. Gasoline
Select: ''')
        if ans_refill == '0': #ans_refill이 0이면 디젤 충전준비
            print('''Based on your rating %d, the discount ratio is %.2f%%
The base unit buying price of Diesel for today is $%.2f,
so the discount unit buying price will be $%.2f''' % (self.rating, min(max(0, self.rating / 2), 30), self.Diesel_selling_price * 0.9, (self.Diesel_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01)))
            
            while True:
                oil_buy = int(input("\nYou have $%.2f. Amount of diesels to buy (liters): " % (self.money)))
                if oil_buy<0: #입력이 0보다 작으면 탈출
                    break
            
                if self.money >= (self.Diesel_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy: #가진 돈이 충분하면 주유소 디젤 탱크 충전
                    print("Money: $%.2f -> $%.2f \nDiesel refilled: %d Liters -> %d Liters" % (self.money, self.money - (self.Diesel_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy, self.Diesel, self.Diesel + oil_buy))
                    self.money -= (self.Diesel_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy
                    self.Diesel += oil_buy
                    break
                
                else: #가진 돈이 부족하면 오류표출
                    print("You don't have enough money")
                    continue
                
        elif ans_refill == '1': #ans_refill이 0이면 가솔린 충전준비
            print('''Based on your rating %d, the discount ratio is %.2f%%
The base unit buying price of Gasoline for today is $%.2f,
so the discount unit buying price will be $%.2f''' % (self.rating, min(max(0, self.rating / 2), 30), self.Gasoline_selling_price * 0.9, (self.Gasoline_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01)))
            
            while True: #입력이 0보다 작으면 탈출
                oil_buy = int(input("\nYou have $%.2f. Amount of gasolines to buy (liters): " % (self.money)))
                if oil_buy<0:
                    break
            
                if self.money >= (self.Gasoline_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy: #가진 돈이 충분하면 주유소 가솔린 탱크 충전
                    print("Money: $%.2f -> $%.2f \nGasoline refilled: %d Liters -> %d Liters" % (self.money, self.money - (self.Gasoline_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy, self.Gasoline, self.Gasoline + oil_buy))
                    self.money -= (self.Gasoline_selling_price * 0.9) * (1 - min(max(0, self.rating / 2), 30)*0.01) * oil_buy
                    self.Gasoline += oil_buy
                    break
                
                else: #가진 돈이 부족하면 오류표출
                    print("You don't have enough money")
                    continue
        

    def print_status(self): # 현재 상태를 출력하는 함수
        print("\n---------STATUS---------")
        print("Day: ", self.day)
        print("Rating: ", self.rating)
        print("Money: $%.2f" % self.money)
        print("# Customers handled for today: ", self.today_num)
        print("Diesel left: ", int(self.Diesel),  "Litters")
        print("Gasoline left: ", int(self.Gasoline),"Litters")

    def default_screen(self): # 초기화면 출력 및 초기화면에서 (0. Wait for a vehicle) 제외한 나머지 입력을 처리하는 함수
        print('''\n---------GAS STATION---------
0. Wait for a vehicle
1. Refill tanks
2. Show current status
3. Go to the next day
4. End Game''')
        while True:
            sel=input("Select:")
            if sel == '0': #입력이 0이면 self.customer의 값을 1로 변경
                self.customer = '1'
            
            elif sel == '1': #입력이 1이면 주유소 탱크 충전 준비
                self.refill()
                return False

            elif sel == '2': #입력이 2면 현재 상태 출력
                self.print_status()
                return False

            elif sel == '3': #입력이 3이면 다음날로 넘어갈 준비
                if self.today_num<3: #하루 방문 고객수가 3보다 작으면 오류 표출
                    print("You have to handle at least three customers. (%d / 3)" %self.today_num)
                else: #하루 방문 고객수가 3보다 크면 다음날로 넘어감
                    self.next()
                return False

            elif sel == '4': #입력이 4면 다음날로 넘어갈 준비
                if self.money<5000.00: #모은 돈이 5000.00달러 미만이면 오류 표출
                    print("You should have at least $5000 to finish the game.")
                    print("You have: $%.2f" %self.money)
                    return False
                else: #모은 돈이 5000.00달러 이상이면 게임 종료
                    print("\n---------Summary---------")
                    print("Rating: %d" %self.rating)
                    print("Money: $%.2f" %self.money)
                    print("Total customers handled: %d" %self.total_num)
                    print("-----------------------------")
                    print("\nYou win!")
                    return True

            else: #0~4이외의 값이 들어오면 오류표출
                print("\nWrong input!")
                continue
            
            break
            
                      
    def serve(self): # 초기화면에서 (0. Wait for a vehicle) 선택 시, 실행되는 함수 차량 도착 시 요구하는 서비스를 랜덤으로 결정하고, 이에 대한 응대
        print("\nWaiting...", end='') #waiting 표시
        for i in range(3):
            print(".", end='')
            time.sleep(0.3)
        print()
        
        car=random.randint(1,6) #변수 car에 1~6의 정수중 임의의 하나를 저장
        if car == 1: #car가 1이면 차종이 SUV
            self.vehicle_type = SUV()
            
        elif car == 2: #car가 2면 차종이 Hybrid
            self.vehicle_type = Hybrid()
            
        elif car== 3 or car == 4: #car가 3또는 4면 차종이 Bus
            self.vehicle_type = Bus()
            
        else: #car가 5또는 6이면 차종이 Truck
            self.vehicle_type = Truck()

        select=random.randint(1,5) #변수 select에 1~5의 정수중 하나를 임의로 저장
        if select == 3: #select가 3이면 차종에 맞게 서비스 요청
            self.vehicle_type.printInfo()
            self.vehicle_type.upgrade_claim()
            ans=int(input('''\n0. Yes
1. No
Select: '''))
            
            if ans == 0: #서비스 요청 시 답변이 Yes
                if self.money>=self.vehicle_type.service_price: #가진 돈이 서비스에 필요한 돈보다 많으면 돈이 줄고 평판이 증가
                    self.vehicle_type.upgrade()
                    print("Money: $%.2f -> $%.2f" %(self.money, self.money - self.vehicle_type.service_price))
                    print(self.rs["for_free"][1])
                    self.del_rating=self.rs["for_free"][0]
                    self.money-=self.vehicle_type.service_price
                    self.state_update()
                    
                else: #가진 돈이 서비스에 필요한 돈보다 적으면 평판 감소
                    print("You don’t have enough money!")
                    print("Money: $%.2f, Required: $%d" %(self.money, self.vehicle_type.service_price))
                    print(self.rs['let_go'][1])
                    self.del_rating=self.rs['let_go'][0]
                    self.state_update()
                    
            else: #서비스 요청 시 답변이 No면 평판이 감소
                print(self.rs['let_go'][1])
                self.del_rating=self.rs['let_go'][0]
                self.state_update()

            self.today_num+=1 #오늘 방문한 고객 수 1증가
            self.total_num+=1 #전체 방문한 고객 수 1증가
            self.customer=None #고객 없음 상태로 변경

        else: #select가 3이 아니면 주유 준비
            self.vehicle_type.printInfo() #차량 정보 표출

            if self.vehicle_type.full == True: #self.vehicle_type.full이 True면 운전자가 Full로 채워달라고 요구
                print("Driver: please make it full!")
                
            else: ##self.vehicle_type.full이 True가 아니면 넣고 싶은 기름의 양 표출
                print("Driver: I'd like %d liters, please." %self.vehicle_type.needed)

            print("Diesel left: %d Liters, Gasoline left: %d Liters" %(self.Diesel, self.Gasoline))
            
            while True:
                ans_serve=input('''\n0. Change fueling method
1. Start fueling
2. Let go
Select: ''')
                if ans_serve == '0': #ans_serve가 0이면 Change fueling method 실행
                    print("\nCurrent Method: %s / %d Liters." %(self.init_oiltype, self.init_oil))
                    
                    while True:
                        ans_method=input('''\n0. Toggle fuel type
1. Change the amount of fuel
2. Finish
Select: ''')
                        if ans_method == '0': #ans_method가 0이면 
                            if self.init_oiltype == 'Gasoline': #현재 주유방식의 유종이 가솔린이면 디젤로 변경
                                self.init_oiltype = 'Diesel'
                                
                            else: #현재 주유방식의 유종이 디젤이면 가솔린으로 변경
                                self.init_oiltype = 'Gasoline'

                            print("Fuel type changed: %s" %(self.init_oiltype))
                            
                        elif ans_method == '1': #ans_method가 1이면
                            while True:
                                ans_of_1=input("Enter 'F' (full), or the amount of liters to fuel: ") #넣고싶은 기름의 양 입력받음
                                if ans_of_1 == 'F': #F를 입력받으면 주유방식의 연료량을 넣을 수 있는 최대한의 양으로 설정
                                    self.init_oil=self.vehicle_type.capacity-self.vehicle_type.cur_fuel
                                    print("Fueling method changed: Full")
                                    break

                                elif ans_of_1.isdigit()== True: #양의 정수를 입력받으면 주유방식의 연료량을 입력받은 값으로 설정
                                    self.init_oil = int(ans_of_1)
                                    print("Fueling method changed: %d Liters" %self.init_oil)
                                    break

                                else: #나머지를 입력받으면 오류 표출
                                    print("Wrong input!")

                        elif ans_method == '2': #ans_method가 2면 탈출
                            break

                elif ans_serve == '1': #ans_serve가 1이면 주유시작
                        print("Checking the conditions...")
                        if  self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "1-1": #self.vehicle_type.fuel의 리턴값이 1-1이면 가솔린 기름부족 오류표출 후 평판 업데이트
                            print('''Fuel type: Gasoline
Amount of Gasoline in the tank: %d Liters, Tried: %d Liters''' % (self.Gasoline, self.init_oil))
                            print(self.rs["not_enough"][1])
                            self.del_rating=self.rs["not_enough"][0]
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "1-2": #self.vehicle_type.fuel의 리턴값이 1-2면 정상적으로 가솔린 주유 후 평판 업데이트
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.vehicle_type.needed*self.Gasoline_selling_price))
                            print("Gasoline: %d Liters -> %d Liters" %(self.Gasoline, self.Gasoline-self.vehicle_type.needed))
                            print()
                            print(self.rs["good_job"][1])
                            self.del_rating=self.rs["good_job"][0]
                            self.money+=self.vehicle_type.needed*self.Gasoline_selling_price
                            self.Gasoline-=self.vehicle_type.needed
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "1-3": #self.vehicle_type.fuel의 리턴값이 1-3이면 가솔린 기름넘침 오류표출 후 평판 업데이트
                            print("Fuel type: Gasoline")
                            print("Maximum amount to fuel: %d Liters, Tried: %d Liters" %(self.vehicle_type.capacity-self.vehicle_type.cur_fuel, self.init_oil))
                            print()
                            print(self.rs["overflow"][1])
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.Gasoline_selling_price*(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)))
                            print("Gasoline: %d Liters -> %d Liters" %(self.Gasoline, self.Gasoline-(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)))
                            self.del_rating=self.rs["overflow"][0]
                            self.money+=self.Gasoline_selling_price*(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)
                            self.Gasoline-=(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "1-4": #self.vehicle_type.fuel의 리턴값이 1-4면 가솔린 주유 양 다름 오류표출 후 평판 업데이트
                            print("Fuel type: Gasoline")
                            print("Requested: %d Liters, Tried: %d Liters" %(self.vehicle_type.needed, self.init_oil))
                            print()
                            print(self.rs["different"][1])
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.Gasoline_selling_price*self.init_oil))
                            print("Gasoline: %d Liters -> %d Liters" %(self.Gasoline, self.Gasoline-self.init_oil))
                            self.del_rating=self.rs["different"][0]
                            self.money+=self.Gasoline_selling_price*self.init_oil
                            self.Gasoline-=self.init_oil
                            self.state_update()

                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "2-1": #self.vehicle_type.fuel의 리턴값이 2-1이면 가솔린 유종 다름 오류표출 후 평판 업데이트
                            print("Requested: Gasoline, Selected: Diesel")
                            print(self.rs["wrong_fuel"][1])
                            self.del_rating=self.rs["wrong_fuel"][0]
                            self.state_update()

                        elif  self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "0-1": #self.vehicle_type.fuel의 리턴값이 0-1이면 디젤 기름부족 오류표출 후 평판 업데이트
                            print('''Fuel type: Diesel
Amount of Diesel in the tank: %d Liters, Tried: %d Liters''' % (self.Diesel, self.init_oil))
                            print(self.rs["not_enough"][1])
                            self.del_rating=self.rs["not_enough"][0]
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "0-2": #self.vehicle_type.fuel의 리턴값이 0-2면 정상적으로 디젤 주유 후 평판 업데이트
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.vehicle_type.needed*self.Diesel_selling_price))
                            print("Diesel: %d Liters -> %d Liters" %(self.Diesel, self.Diesel-self.vehicle_type.needed))
                            print()
                            print(self.rs["good_job"][1])
                            self.del_rating=self.rs["good_job"][0]
                            self.money+=self.vehicle_type.needed*self.Diesel_selling_price
                            self.Diesel-=self.vehicle_type.needed
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "0-3": #self.vehicle_type.fuel의 리턴값이 0-3이면 디젤 기름넘침 오류표출 후 평판 업데이트
                            print("Fuel type: Diesel")
                            print("Maximum amount to fuel: %d Liters, Tried: %d Liters" %(self.vehicle_type.capacity-self.vehicle_type.cur_fuel, self.init_oil))
                            print()
                            print(self.rs["overflow"][1])
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.Diesel_selling_price*(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)))
                            print("Diesel: %d Liters -> %d Liters" %(self.Diesel, self.Diesel-(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)))
                            self.del_rating=self.rs["overflow"][0]
                            self.money+=self.Diesel_selling_price*(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)
                            self.Diesel-=(self.vehicle_type.capacity-self.vehicle_type.cur_fuel)
                            self.state_update()
                            
                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "0-4": #self.vehicle_type.fuel의 리턴값이 0-4면 디젤 주유 양 다름 오류표출 후 평판 업데이트
                            print("Fuel type: Diesel")
                            print("Requested: %d Liters, Tried: %d Liters" %(self.vehicle_type.needed, self.init_oil))
                            print()
                            print(self.rs["different"][1])
                            print("Money: $%.2f -> $%.2f"%(self.money, self.money+self.Diesel_selling_price*self.init_oil))
                            print("Diesel: %d Liters -> %d Liters" %(self.Diesel, self.Diesel-self.init_oil))
                            self.del_rating=self.rs["different"][0]
                            self.money+=self.Diesel_selling_price*self.init_oil
                            self.Diesel-=self.init_oil
                            self.state_update()    

                        elif self.vehicle_type.fuel(self.init_oiltype, self.init_oil, self.Diesel, self.Gasoline) == "2-0": #self.vehicle_type.fuel의 리턴값이 2-0이면 디젤 유종 다름 오류표출 후 평판 업데이트
                            print("Requested: Diesel, Selected: Gasoline")
                            print(self.rs["wrong_fuel"][1])
                            self.del_rating=self.rs["wrong_fuel"][0]
                            self.state_update()
                        self.today_num+=1 #오늘 방문한 고객 수 1증가
                        self.total_num+=1 #전체 방문한 고객 수 1증가
                        self.customer=None #고객 없음 상태로 변경
                        break

                else: #ans_serve가 2면 차량을 돌려보냄
                    print()
                    print(self.rs["let_go"][1])
                    self.del_rating=self.rs["let_go"][0]
                    self.state_update()
                    self.today_num+=1 #오늘 방문한 고객 수 1증가
                    self.total_num+=1 #전체 방문한 고객 수 1증가
                    self.customer=None #고객 없음 상태로 변경
                    break               


    def price_update(self): # 기름 가격을 변동하는 함수
        self.Previous_Gasoline_selling_price = self.Gasoline_selling_price
        self.Previous_Diesel_selling_price = self.Diesel_selling_price
        self.Gasoline_selling_price*=(1 + random.uniform(-0.1, 0.1))
        self.Diesel_selling_price*=(1 + random.uniform(-0.1, 0.1))
        print("Gasoline unit selling price: $%.2f -> $%.2f" %(self.Previous_Gasoline_selling_price, self.Gasoline_selling_price))
        print("Diesel unit selling price: $%.2f -> $%.2f" %(self.Previous_Diesel_selling_price, self.Diesel_selling_price))


    def next(self): # 다음 날로 이동하는 함수
        print("Day %d finished." %self.day)
        self.day+=1 #날짜 1일 증가
        self.today_num=0 #오늘 방문한 고객수 초기화
        self.price_update() #기름 가격 업데이트
        

class Car:
    # 인스턴스 변수
    def __init__(self): #변수 선언
        self.fuel_type # 연료 종류(가솔린, 디젤)
        self.vehicle_type # 자동차 종류(트럭, 버스, SUV, 하이브리드)
        self.capacity # 연료통 크기
        self.cur_fuel # 현재 남은 용량
        self.needed # 주유 요구 시, 채워달라고 요청하는 연료의 양
        self.full # 주유 요구 시, 연료통을 가득 채워달라고 하는지 여부

    # 메서드
    def __init__(self):
        self.cal_fuel()


    def cal_fuel(self): # 남은 기름의 양 계산 및 full 여부
        self.cur_fuel = int(self.capacity * random.uniform(0.1, 0.4))
        if random.randint(1, 4) == 1: 
            self.full = True
            self.needed = self.capacity - self.cur_fuel
            
        else:
            self.full = False
            self.needed = ((self.capacity - self.cur_fuel) * random.uniform(0.5, 0.8) // 5) * 5


    def printInfo(self): # 차량 정보 출력
        print("\n<<Vehicle Info>>")
        print(f"Fuel type: {self.fuel_type}, Vehicle type: {self.vehicle_type}, Fuel: {self.cur_fuel} / {self.capacity}")


    def fuel(self, init_oiltype, init_oil, Diesel, Gasoline): # 지정한 주유 방식대로 차량에 기름을 넣는 함수
        if self.fuel_type == init_oiltype: #지정 주유 유종이 차량의 유종과 같으면
            if self.fuel_type == "Gasoline": #차량의 유종이 가솔린일때 
                if init_oil > Gasoline: #주유하려는 양이 주유소의 기름 양보다 많으면
                    return "1-1" #"1-1"반환
                    
                elif self.needed == init_oil: #주유하려는 양이 원하는 기름의 양과 같으면
                    return "1-2" #"1-2"반환
                
                elif init_oil>self.capacity-self.cur_fuel: #주유하려는 양이 차량에 채울 수 있는 최대 기름 양보다 많으면
                    return "1-3" #"1-3"반환
                
                elif init_oil != self.needed: #위의 경우를 다 제외하고 주유하려는 양과 원하는 기름의 양이 다르면 
                    return "1-4" #"1-4"반환
                
            elif self.fuel_type == "Diesel": #차량의 유종이 디젤일때 
                if init_oil > Diesel: #주유하려는 양이 주유소의 기름 양보다 많으면
                    return "0-1" #"0-1"반환
                
                elif self.needed == init_oil: #주유하려는 양이 원하는 기름의 양과 같으면
                    return "0-2" #"0-2"반환
                
                elif init_oil>self.capacity-self.cur_fuel: #주유하려는 양이 차량에 채울 수 있는 최대 기름 양보다 많으면
                    return "0-3" #"0-3"반환
                
                elif init_oil != self.needed: #위의 경우를 다 제외하고 주유하려는 양과 원하는 기름의 양이 다르면
                    return "0-4" #"0-4"반환
                
        else: #지정 주유 유종이 차량의 유종과 다르면
            if self.fuel_type == "Gasoline": #차량의 유종이 가솔린이면
                return "2-1" #"2-1"반환
            else: #차량의 유종이 디젤이면
                return "2-0" #"2-0"반환
            

class Gasoline_Car(Car): # Car의 클래스를 상속받아 Gasoline_Car클래스 생성
    # 메서드
    def __init__(self):
        super().__init__()
        self.fuel_type = "Gasoline" #fuel_type을 가솔린으로 설정


class Diesel_Car(Car): # Car의 클래스를 상속받아 Diesel_Car클래스 생성
    # 메서드
    def __init__(self):
        super().__init__()
        self.fuel_type = "Diesel" #fuel_type을 디젤로 설정


    def upgrade_claim(self): # DEF 업그레이드 요청
        print("Driver: Refill the DEF, please.")
        print("Provide some DEF for free? (costs $50 yet increases rating by 3)")


    def upgrade(self) : # DEF 업그레이드 요청에 응했을 때 실행되는 부분
        print("You provided some DEF for free")


class SUV(Gasoline_Car): # Gasoline_Car의 클래스를 상속받아 SUV클래스 생성
    # 메서드
    def __init__(self):
        self.vehicle_type = "SUV" #vehicle_type을 SUV로 설정
        self.capacity = 80 #차량의 기름탱크의 용량을 80으로 설정
        self.service_price=100 #엔진오일 서비스의 가격을 100으로 설정
        super().__init__()
        
    def upgrade_claim(self): # 엔진오일 업그레이드 요청
        print("Driver: An oil change, please.")
        print("Change the engine oil for free? (costs $100 yet increases rating by 3)")

    def upgrade(self) : # 엔진오일 업그레이드 요청에 응했을 때 실행되는 부분
        print("You replaced the engine oil for free")

class Hybrid(Gasoline_Car): # Gasoline_Car의 클래스를 상속받아 Hybrid 클래스 생성
    # 메서드
    def __init__(self):
        self.vehicle_type = "Hybrid" #vehicle_type을 Hybrid로 설정
        self.capacity = 60 #차량의 기름탱크의 용량을 60으로 설정
        self.service_price=300 #타이어 서비스의 가격을 300으로 설정
        super().__init__()

    def upgrade_claim(self): # 타이어 업그레이드 요청
        print("Driver: My car has flat tires...")
        print("Change the tires for free? (costs $300 yet increases rating by 3)")

    def upgrade(self) : # 타이어 업그레이드 요청에 응했을 때 실행되는 부분
        print("You provided some tires for free")

class Bus(Diesel_Car): # Diesel_Car의 클래스를 상속받아 Bus클래스 생성
    # 메서드
    def __init__(self): 
        self.vehicle_type = "Bus"  #vehicle_type을 Bus로 설정
        self.capacity = 100 #차량의 기름탱크의 용량을 100으로 설정
        self.service_price=50 #DEF 서비스의 가격을 50으로 설정
        super().__init__()

class Truck(Diesel_Car): # Diesel_Car의 클래스를 상속받아 Truck클래스 생성
    # 메서드
    def __init__(self):
        self.vehicle_type = "Truck"  #vehicle_type을 Truck으로 설정
        self.capacity = 300 #차량의 기름탱크의 용량을 300으로 설정
        self.service_price=50 #DEF 서비스의 가격을 50으로 설정
        super().__init__()



S = Station()
while True:
    if S.customer == None: # 차량이 도착하기 전(초기 상태 포함)
        if S.default_screen(): # 4. End Game 조건이 만족된 경우 True를 반환하여 프로그램 종료
            break

    else: # 차량이 도착한 경우 S.serve() # 차량의 요구에 따라 응대
        S.serve()
