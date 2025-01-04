#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import time
import random


class GameObject:
    # tkinter의 coords, delete, move 함수 참고
    # canvas와 item 초기화
    def __init__(self, canvas, item): # canvas, item을 초기화하는 함수
        self.canvas = canvas # canvas를 입력 받는 변수
        self.item = item # canvas에 그려지는 오브젝트
        
    # canvas에서 item의 위치값 리턴    
    def get_position(self): # 특정 item의 위치 값을 반환하는 함수
        return self.canvas.coords(self.item)
    
    # canvas 내에서 item 삭제
    def delete(self): # 특정 item을 삭제
        self.canvas.delete(self.item)
        
    # canvas 내에서 item을 (x, y)만큼 이동
    def move(self, x, y): # 특정 item을 (x, y)만큼 이동
        self.canvas.move(self.item, x, y)


class Quadrangle(GameObject):
    # 부모 클래스 초기화 함수로 canvas와 item 정의(item은 사각형 전달; tkinter의 create_rectangle() 참고)
    # self.x, self.y, self.width, self.height, self.color 정의
    def __init__(self, canvas, x, y, width, height, color): # GameObject class를 이용하여 변수 초기화
        self.color = color # 사각형의 색상
        self.item = canvas.create_rectangle(x - width/2, y + height/2, x + width/2, y - height/2, fill=self.color) #item 정의
        self.x = x #사각형의 x위치
        self.y = y # 사각형의 y 위치
        self.width = width # 사각형의 가로 길이
        self.height = height # 사각형의 세로 길이
        super().__init__(canvas, self.item)

        
              
class Player(Quadrangle):
    # 부모 클래스 초기화 함수를 이용하여 Player 초기화 (문제 출제 내용의 width, height, color 참고)
    def __init__(self, canvas, x, y): # Qudrangle class를 이용하여 변수 초기화
        width=50
        height=50
        color="blue"
        super().__init__(canvas,x,y, width, height, color)
        self.state = 0  # player의 상태; 0: Running, 1: Jumping, 2: GameOver
            
    # target object의 position을 받아 Player와의 충돌 여부에 관해 리턴하는 함수 (AABB Collision Detection 참고)
    def check_collision(self, tPos): # 플레이어와 타겟 오브젝트가 충돌이 나면 1, 일어나지 않으면 0을 리턴하는 함수
        player_pos = self.get_position()
        player_left = player_pos[0]
        player_top = player_pos[1]
        player_right = player_pos[2]
        player_bottom = player_pos[3]

        const_x = max(player_left, min((tPos[0]+tPos[2])/2, player_right))
        const_y = max(player_top, min((tPos[1]+tPos[3])/2, player_bottom))
        const_distance = ((const_x-((tPos[0]+tPos[2])/2))**2 + (const_y-((tPos[1]+tPos[3])/2))**2)**0.5

        if const_distance < tPos[4]:
            result=1
        else:
            result=0
        return result
    

class Terrain(Quadrangle):
    # 부모 클래스 초기화 함수를 이용하여 Terrain 초기화 (문제 출제 내용의 width, height, color 참고)
    def __init__(self, canvas, x, y): # Qudrangle class를 이용하여 변수 초기화
        super().__init__(canvas, x, y, 250, 200, 'green')


class Circle(GameObject):
    # 부모 클래스 초기화 함수로 canvas와 item 정의(item은 사각형 전달; tkinter의 create_oval() 참고)
    # self.x, self.y, self.radius, self.color 정의
    def __init__(self, canvas, x, y, radius, color): # GameObject class를 이용하여 변수 초기화
        self.x = x # x좌표
        self.y = y # y좌표
        self.color = color # 원의 색
        self.radius = radius # 원의 반지름
        self.item = canvas.create_oval(self.x - self.radius, self.y + self.radius, self.x + self.radius, self.y - self.radius, fill=self.color)
        super().__init__(canvas, self.item)

        

class Coin(Circle):
    # 부모 클래스 초기화 함수를 이용하여 Coin 초기화 (문제 출제 내용의 radius, color 참고)
    def __init__(self, canvas, x, y): # Circle class를 이용하여 변수 초기화
        radius= 10
        color='yellow'
        super().__init__(canvas, x, y, radius, color)
        
class FireBall(Circle):
    # 부모 클래스 초기화 함수를 이용하여 FireBall 초기화 (문제 출제 내용의 radius, color 참고)
    def __init__(self, canvas, x, y): # Circle class를 이용하여 변수 초기화
        radius = 15
        color = 'red'
        super().__init__(canvas, x, y, radius, color)


# tk.Frame 상속
class Game(tk.Frame):
    
    def __init__(self, master, width, height): # Canvas 화면 창을 띄우는 함수
        super(Game, self).__init__(master)
        self.width = width # 화면 창의 가로 길이
        self.height = height # 화면 창의 세로 길이
        self.canvas = tk.Canvas(self, bg = 'white', width = self.width, height = self.height) # 흰색 창을 가지는 canvas
        self.canvas.pack(fill="both", expand=True)     
        self.pack()
        
        self.setup_game()
        
    def setup_game(self): # 게임 기본 맵 및 기능 세팅
        self.gameInit()
        self.canvas.bind('<space>', lambda _: self.update_jumping())  # space key 입력시 self.update_jumping() 호출
        self.canvas.focus_set()
        self.game_loop()
    
    def gameInit(self): # 게임에서 동작하는 파라미터 및 맵 초기화
        self.end_font = ('Helvetica', '40')         # END text의 font로 이용
        self.score_font = ('Helvetica', '15')       # Score text의 font로 이용
        
        self.score = 0 # Coin 획득 점수
        self.mapSpeed = -5 # player를 제외한 오브젝트들의 이동 속도(우측좌측)
        self.jumpSpeed = 0    # player의 점프 속도
        
        self.terrains = [] # map의 모든 terrain들을 포함하는 리스트
        self.fireballs = [] # map의 모든 fireball들을 포함하는 리스트
        self.coins = [] # map의 모든 coin들을 포함하는 리스트
        
        self.player = Player(self.canvas, 200, 475)       
        
        terrain1 = Terrain(self.canvas, 125, 600)
        terrain2 = Terrain(self.canvas, 375, 600)
        terrain3 = Terrain(self.canvas, 625, 600)
        terrain4 = Terrain(self.canvas, 875, 600)
        terrain5 = Terrain(self.canvas, 1125, 600)
        terrain6 = Terrain(self.canvas, 1375, 600)
        terrain7 = Terrain(self.canvas, 1625, 600)
        self.terrains = [terrain1, terrain2, terrain3, terrain4, terrain5, terrain6, terrain7]

        # Create fireballs
        fireball1 = FireBall(self.canvas, 1200, self.random_posY())
        self.fireballs = [fireball1]

        # Create coins
        coin1 = Coin(self.canvas, 1200, self.random_posY())
        self.coins = [coin1]

        # Create score text
        self.score_text = self.canvas.create_text(1100, 50, text="SCORE: 0", font=self.score_font, fill="black") # Coin 획득 점수를 나타내는 텍스트

        # Create end text
        self.end_text = self.canvas.create_text(self.width/2, self.height/2, text="", font=self.end_font, fill="black") # 게임 종료 시, 나타나는 텍스트
        
    def game_loop(self): # 게임 종료 상태가 아니라면 게임 실행하는 함수
        if(self.player.state != 2):
            self.gameSystem()
            self.after(10, self.game_loop)   # 10ms(초당 100프레임)마다 game_loop() 실행
    

    def gameSystem(self): # 전체적인 게임 동작
        self.move_map()    
        self.manage_map()  
        self.check_gameState()    
    
    def manage_map(self): # terrains, fireballs, coins의 전체적인 맵 관리
        self.manage_terrains()
        self.manage_fireballs()
        self.manage_coins()
    
    # terrain의 동작 내용
    def manage_terrains(self): 
        for terrain in self.terrains: # terrain의 우측면이 화면에 벗어나면 지우고 추가
            if terrain.get_position()[2] <= 0:
                self.terrains.append(Terrain(self.canvas, 1625, 600))
                terrain.delete()
                self.terrains.remove(terrain)
                


                
    # fireball의 동작 내용
    def manage_fireballs(self): # fireball의 우측면이 화면에 벗어나면 지우고 추가
        for fireball in self.fireballs:
            if fireball.get_position()[2] < 0:
                fireball.delete()
                self.fireballs.remove(fireball)
                self.fireballs.append(FireBall(self.canvas, 1200, self.random_posY()))

    
    # coin의 동작 내용
    def manage_coins(self): # coin의 우측면이 화면에 벗어나면 지우고 추가
        for coin in self.coins:
            if coin.get_position()[2] < 0:
                coin.delete()
                self.coins.remove(coin)
                self.coins.append(Coin(self.canvas, 1200, self.random_posY()))
        
    # 1/2 확률로 2가지 중 하나의 y값 리턴
    def random_posY(self): # coin이나 fireball의 생성 시 랜덤한 2개의 위치값을 반환
        num = random.randint(0,1)
        if(num == 0):
            return 400
        else:
            return 450
    
    # jumping, gameover 상태에 따른 동작
    def check_gameState(self): # 게임 종료 상태면 “END” 텍스트 출력 및 점프 상태에 따른 점프 동작 함수를 실행
        if(self.player.state == 2):      # gameover 상태
            self.canvas.itemconfig(self.end_text, text="END") 
        elif(self.player.state == 1):    # jumping 상태
            self.jumping()         
    
    # space 입력시 변수 초기화
    def update_jumping(self): # ‘space’ key 입력 시, 실행되는 함수, 점프 상태로 업데이트하는 함수
        if self.player.state == 0:
            self.jump_speed = 15
            self.player.state = 1
    
    # 점프 구현
    def jumping(self): # jump 동작 구현
        if self.jump_speed >= -15:
            self.player.move(0, -self.jump_speed)
            self.jump_speed -= 1
        else:
            self.jump_speed = 0
            self.player.state = 0
    
    # terrains, coins는 mapSpeed의 속도로 이동하며, fireball은 mapSpeed의 2배 속도로 이동함
    def move_map(self): # terrains, coins는 mapSpeed의 속도로 이동하며, fireball은 mapSpeed의 2배 속도로 이동함
        for terrain in self.terrains: #terrain 이동
            self.canvas.move(terrain.item, self.mapSpeed, 0)
        for fireball in self.fireballs: #fireball 이동
            self.canvas.move(fireball.item, self.mapSpeed * 2, 0)
            fireball_pos = fireball.get_position()
            fireball_pos.append(15)
            if self.player.check_collision(fireball_pos) == 1: #fireball에 Player 충돌 시 게임종료 
                self.player.state = 2
        for coin in self.coins: #coin 이동
            self.canvas.move(coin.item, self.mapSpeed, 0)
            coin_pos = coin.get_position()
            coin_pos.append(10)
            if self.player.check_collision(coin_pos) == 1: #coin에 Player 충돌 시 score업데이트, 코인 삭제 후 재생성
                coin.delete()  # Remove the coin from the list
                self.coins.remove(coin)
                self.score += 1  # Increase the score
                self.canvas.itemconfig(self.score_text, text="SCORE: {}".format(self.score))  # Update the score text
                self.coins.append(Coin(self.canvas, 1200, self.random_posY()))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Assignment4_20230185')
    game = Game(root, 1200, 700)
    game.mainloop()

