import random #random모듈 불러오기
import os #os모듈 불러오기

while True:
    size=int(input("Choose the puzzle size: ")) #사용자로부터 n*n 퍼즐의 사이즈를 입력받음
    if (size<3) or (size>6): #n이 3보다 작거나 6보다 크면
          print("Wrong size!") #오류를 표출 후
          continue #다시 입력받음
    else: #n이 3이상 6이하이면
        print("Enjoy the puzzle!") #"Enjoy the puzzle!"을 표출 
        break 
    
def create_random_puzzle(size):
    real_puzzle = [[i for i in range(size)] for j in range(size)] #n*n 크기의 2차원 리스트를 생성
    nums = [i for i in range(1,size**2)] #1~n^2-1까지의 정수가 들어있는 리스트 생성
    nums.append("*") #nums 리스트에 '*'추가
    random.shuffle(nums) #nums 리스트를 랜덤하게 섞음

    for i in range(size): #real_puzzle 리스트의 [i][j]번 원소에 nums리스트의 원소를 순서대로 대입
        for j in range(size):
            real_puzzle[i][j]=nums[size*i+j]
    return real_puzzle #real_puzzle 리스트를 반환

puzzle=create_random_puzzle(size) #변수 puzzle에 create_random_puzzle(size) 함수의 반환값을 대입 
            
def print_puzzle(puzzle, size):
    unit="+----" #슬라이딩 퍼즐 칸 양식의 기본단위 지정
    for i in range(size): #행의 개수만큼 반복
        print("%s+"%(size*unit)) #열의 개수만큼 unit을 반복출력
        print("|", end="")
        for j in range(size): #빙고판에 숫자를 차례대로 출력
            print(" %2s |" %(puzzle[i][j]),end="")
        print()
    print("%s+"%(size*unit)) #열의 개수만큼 unit을 반복출력
    
def find_blank(puzzle, size):
    position=[(i,j) for i in range(size) for j in range(size) if puzzle[i][j]=='*'] #2차원 리스트의 [i][j]번 원소에 '*'이 있는지 확인 후 i, j를 position 리스트에 대입
    return(position[0]) #position 리스트의 0번 원소를 반환

def swap_blocks(puzzle, block_a, block_b):
    a1=int(block_a[0:1]) #block_a 문자열의 첫 번째 글자를 슬라이싱
    a2=int(block_a[1:2]) #block_a 문자열의 두 번째 글자를 슬라이싱
    b1=int(block_b[0:1]) #block_b 문자열의 첫 번째 글자를 슬라이싱
    b2=int(block_b[1:2]) #block_b 문자열의 두 번째 글자를 슬라이싱
    puzzle[a1][a2],puzzle[b1][b2] = puzzle[b1][b2],puzzle[a1][a2] #(a1, a2)의 퍼즐 원소과 (b1, b2)의 퍼즐 원소를 서로 교환

def move_blank_block(puzzle, size, command, blank):
    p1=blank[0] #변수 p1에 '*'이 들어있는 좌표의 행의 좌표값을 대입
    p2=blank[1] #변수 p2에 '*'이 들어있는 좌표의 열의 좌표값을 대입
    if (command=='w'): #만약 command가 w라면
        puzzle[p1][p2],puzzle[p1-1][p2] = puzzle[p1-1][p2],puzzle[p1][p2] #'*'이 들어있는 칸과 그 윗 칸의 퍼즐 원소를 교환
    elif (command=='a'): #만약 command가 a라면
        puzzle[p1][p2],puzzle[p1][p2-1] = puzzle[p1][p2-1],puzzle[p1][p2] #'*'이 들어있는 칸과 그 왼쪽 칸의 퍼즐 원소를 교환
    elif (command=='s'): #만약 command가 s라면
        puzzle[p1][p2],puzzle[p1+1][p2] = puzzle[p1+1][p2],puzzle[p1][p2] #'*'이 들어있는 칸과 그 아랫 칸의 퍼즐 원소를 교환
    elif (command=='d'): #만약 command가 d라면
        puzzle[p1][p2],puzzle[p1][p2+1] = puzzle[p1][p2+1],puzzle[p1][p2] #'*'이 들어있는 칸과 그 오른쪽 칸의 퍼즐 원소를 교환
        
def create_from_file(filename):
    file=open(filename, 'r') #filename이라는 파일명을 가진 파일을 읽기모드로 열기
    filelist=file.readlines() #file의 모든 내용을 읽어들여 리스트로 저장
    size=int(filelist[0].strip()) #filelist 리스트의 0번 원소의 값을 변수 size에 정수형으로 저장
    puzzle = [[j for j in i.strip().split()] for i in filelist[1:]] #filelist 리스트의 1번 원소부터 각 원소안의 숫자들을 공백을 기준으로 분리하여 2차원 리스트를 형성
    return puzzle, size #puzzle과 size를 반환

def is_valid(puzzle, size):
    valid_numbers = [i for i in range(1,size**2)] #유효한 숫자들의 모음
    flatten_puzzle=[y for x in puzzle for y in x] #puzzle 2차원 리스트를 1차원 리스트로 해체
    
    if '*' not in flatten_puzzle: #flatten_puzzle 리스트 안에 빈 블록('*')이 없는 경우(3에 해당)
        return False #False 반환
    
    elif sorted(list(map(int, sorted([x for x in flatten_puzzle if x != '*'])))) != valid_numbers: #flatten_puzzle 리스트안에서 '*'을 제외한 숫자들을 크기순서대로 배열한 리스트와 valid_numbers 리스트가 같지 않으면(1, 2에 해당)
        return False #False 반환
    
    elif len(puzzle) != size: #puzzle 2차원 리스트의 행의 개수가 size와 다르면 (4에 해당)
        return False #False 반환
    
    for i in puzzle: #puzzle 2차원 리스트의 각 행에 대해서
        if len(i) != size: #각 행의 원소의 개수(열의 개수)가 size와 다르면 (5에 해당)
            return False #False 반환
        
    return True #나머지 경우에는 True를 반환

def is_solved(puzzle, size):
    answer = [[i for i in range(size)] for j in range(size)] #n*n 크기의 2차원 리스트를 생성
    num=[i for i in range(1,size**2)] #1~n^2-1까지의 정수가 순서대로 들어있는 리스트 생성
    num.append("*") #num 리스트에 '*'추가
    puzzle = [[int(x) if x != '*' else x for x in y] for y in puzzle] #puzzle 2차원 리스트 안에서 '*'을 제외하고 모든 원소를 정수형으로 변환
    for i in range(size): #answer 리스트의 [i][j]번 원소에 nums리스트의 원소를 순서대로 대입
        for j in range(size):
            answer[i][j]=num[size*i+j]
    if (puzzle==answer): #puzzle 2차원 리스트와 answer 2차원 리스트가 같으면 
        return True #True를 반환
    else: #나머지 경우면
        return False #False를 반환
    
while True: #계속 반복문을 실행
    print_puzzle(puzzle, size) #print_puzzle 함수를 호출해 puzzle의 현재상태를 출력
    while (is_solved(puzzle, size)==False): #퍼즐이 풀리기 전까지 이 반복문을 실행
        command=input("Enter the command ... (h: help, q: quit): ") #명령어를 입력받아 command에 저장

        if (command=='h'): #만약 command가 'h'라면 도움말을 출력
            print('''w: Move * to UPPER block
s: Move * to LOWER block
a: Move * to LEFT block
d: Move * to RIGHT block
c: use CHANCE
n: Create NEW puzzle (randomly generated puzzle)
f: Create NEW puzzle (import puzzle from txt file)
h: Print help message
q: Quit the puzzle''')
            
        elif (command=='w' or command=='a' or command=='s' or command=='d'): #만약 command가 'w'또는 'a'또는 's'또는 'd'라면 
            blank=list(find_blank(puzzle, size)) #find_blank 함수로 부터 '*'의 좌표값을 전달받아 blank에 list형태로 저장
            if (blank[0]==0) and (command=='w'): #만약 command가 'w'인데 '*'의 행의 좌표값이 0이라면
                print("Can not move the *") #오류 출력
                break
            elif (blank[1]==0) and (command=='a'): #만약 command가 'a'인데 '*'의 열의 좌표값이 0이라면
                print("Can not move the *") #오류 출력
                break
            elif (blank[0]== (size-1)) and (command=='s'): #만약 command가 's'인데 '*'의 행의 좌표값이 size-1 이라면
                print("Can not move the *") #오류 출력
                break
            elif (blank[1]== (size-1)) and (command=='d'): #만약 command가 'd'인데 '*'의 열의 좌표값이 size-1 이라면
                print("Can not move the *") #오류 출력
                break
            else: #나머지 경우에는 빈칸을 이동
                move_blank_block(puzzle, size, command, blank)
                break

        elif (command=='c'): #만약 command가 'c'라면
            while True: #계속 반복문을 실행
                ans=input("Use CHANCE! Choose the blocks: ") #사용자로부터 서로 바꾸고 싶은 두 퍼즐의 좌표값을 입력받아 ans에 저장
                block_a=ans[0:2] #ans의 첫번째 글자에서 두번째 글자를 슬라이싱해서 block_a에 저장
                block_b=ans[3:5] #ans의 세번째 글자에서 다섯번째 글자를 슬라이싱해서 block_b에 저장
                list1= ans.split() #ans를 공백을 기준으로 분리하여 각각 리스트에 저장
                if (((''.join(list1)).isdigit())==False): #ans에 문자열이 포함되어 있으면 오류 표출 후 재입력을 받음
                    print("Wrong input!") #오류 표출 후 재입력을 받음
                    continue
                elif (len(list1)!=2): #띄어쓰기가 하나가 아니면 오류 표출 후 재입력을 받음
                    print("Wrong input!") #오류 표출 후 재입력을 받음
                    continue
                elif (len(list1[0]) != 2) or (len(list1[1]) != 2): #입력받은 각 좌표의 길이가 2가 아니면
                    print("Wrong input!") #오류 표출 후 재입력을 받음
                    continue
                elif ((int(block_a[0:1])<0) or (int(block_a[0:1])>=size)) or ((int(block_a[1:2])<0) or (int(block_a[1:2])>=size)) or ((int(block_b[0:1])<0) or (int(block_b[0:1])>=size)) or ((int(block_b[1:2])<0) or (int(block_b[1:2])>=size)): #입력받은 각 좌표의 좌표값이 범위를 넘어가면
                    print("Wrong input!") #오류 표출 후 재입력을 받음
                    continue
                else: #나머지 경우에는 두 퍼즐의 원소를 바꿈
                    swap_blocks(puzzle, block_a, block_b)
                    break
            break
        
        elif (command == 'n'): #만약 command가 'n'이라면
            while True:
                size=int(input("Choose the puzzle size: ")) #사용자로부터 n*n 퍼즐의 사이즈를 입력받음
                if (size<3) or (size>6): #n이 3보다 작거나 6보다 크면
                      print("Wrong size!") #오류를 표출 후
                      continue #다시 입력받음
                else: #n이 3이상 6이하이면
                    print("Enjoy the puzzle!") #"Enjoy the puzzle!"을 표출
                    break 
            puzzle=create_random_puzzle(size) #변수 puzzle에 create_random_puzzle(size) 함수의 반환값을 대입
            break
        
        elif (command=='f'): #만약 command가 'f'라면
            while True: #계속 반복문을 실행
                filename=input("File Name: ") #사용자로부터 파일명을 입력받아 filename에 저장
                if not os.path.exists(filename): #만약 filename의 파일명을 가진 파일이 존재하지 않으면 
                    print("No file is found") #오류 표출 후 재입력 받음
                    continue
                puzzle, size = create_from_file(filename) #create_from_file 함수로 부터 puzzle값과 size값을 넘겨받아 변수에 저장
                if (is_valid(puzzle, size) == False): #만약 is_valid의 반환값이 False라면 
                    print("Error!") #오류 표출 후 재입력을 받음
                    continue
                else: #나머지 경우(is_valid의 반환값이 True인 경우)에는
                    break #반복문 탈출
            break #반복문 탈출
            

        elif (command=='q'): #만약 command가 'q'라면
            print("Quit the puzzle game.") #"Quit the puzzle game." 출력 후 
            break #반복문 탈출
        
        else: #command가 위의 명령어들 이외의 문자열인 경우에는
            print("Wrong input!") #오류 표출
            
    if (command=='q'): #만약 command가 'q'라면
        break #반복문 탈출
    
    elif (is_solved(puzzle, size)==True): #만약 is_solved의 반환값이 True라면
        print_puzzle(puzzle, size) #퍼즐의 집행상황을 출력 후 
        print("The puzzle is solved.") #"The puzzle is solved."를 출력 후
        break #반복문 탈출

