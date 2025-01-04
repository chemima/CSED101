import random #랜덤 모듈 불러오기
word_list = ['apple', 'april', 'banana', 'blue', 'coral', 'dictionary', 'flower', 'peach', 'strawberry', 'watermelon'] #행맨게임에 나오는 단어 목록

comp_word=random.choice(word_list) #word_list의 단어들 중 하나를 임의로 골라 comp_word에 저장
used=' ' #사용된 알파벳들을 모아놓는 문자열의 초기값
life=10 #Life의 초기값

def reveal_word(comp_word, used):
    for i in comp_word: #comp_word 속 단어의 알파벳 개수만큼 반복
        if i in used: #만약 used에 단어 속 알파벳이 존재한다면
            print(i, end=' ')#알파벳을 출력함
        else: #used에 단어 속 알파벳이 존재하지 않는다면 _를 출력함
            print('_', end=' ')
    
def print_status(comp_word,used,life): #단어를 얼마나 맞췄는지, 무슨 단어를 사용했는지, 남은 life가 얼마인지를 알려줌
    print("---------------------------------------------")
    print("Word: ", end='')
    reveal_word(comp_word, used)
    print("\nUsed:", used)
    print("Life: ", life)
    print("---------------------------------------------")
   
def is_word_guessed(comp_word, used): #단어를 다 맞췄으면 True를, 단어를 다 맞추기 전까진 False를 반환함.
    for l in comp_word: #comp_word 속 단어의 알파벳 개수만큼 반복
        if l not in used: #used 속에 단어가 하나라도 없으면 그대로 False를 반환
            return False
    return True

print("Hangman game starts!") 
while (is_word_guessed(comp_word, used)==False): #단어를 다 맞추기 전까지 이 반복문을 실행
    print_status(comp_word,used,life) 
    a=input("Choose a character: ") #알파벳을 입력받아서 변수 a에 저장
    if a in used: #a가 이미 사용된 글자이면 다시 입력하라는 오류를 반환
        print("You have already checked this character. Try another one.")
        
    elif a in comp_word: #a가 comp_word에 들어있는 알파벳이라면
        used=used+ ' ' +a #used에 a를 추가
        if (is_word_guessed(comp_word, used)==True): #단어를 맞춰 is_word_guessed의 값이 True가 되면
            print("Hangman Survived!")
            while True:
                ans=input("Do you want to play another game?: ")
                if (ans=="yes"): #yes를 입력시 초기값을 재설정 후 반복문 밖으로 나감
                    comp_word=random.choice(word_list)
                    used = ''
                    life = 10
                    break
                elif (ans=="no"): #no를 입력시 is_word_guessed의 값이 True인 상태로 반복문 밖으로 나가기에 반복문이 실행되지 않음
                    print("Quit the Hangman Game.")
                    break
                    
                else: #yes나 no 이외의 다른 글자가 들어오면 오류 표출 후 재입력을 받음
                    print("Wrong input!")
        continue
        
    else: #a가 used에도 없고, 단어속에도 없는 알파벳이라면
        used=used+ ' ' +a #used에 a를 추가
        life=life-1 #life가 1감소
        if life==0: #만약 life가 0이 되버리면
            print("Hangman Die!")
            print("The answer was %s." %(comp_word)) #답을 표출
            while True:
                ans=input("Do you want to play another game?: ")
                if (ans=="yes"): #yes를 입력시 초기값을 재설정 후 반복문 밖으로 나감
                    comp_word=random.choice(word_list)
                    used = ''
                    life = 10
                    break
                elif (ans=="no"): #no를 입력시 "Quit the Hangman Game." 를 출력 후 break
                    print("Quit the Hangman Game.")
                    break
                else: #yes나 no 이외의 다른 글자가 들어오면 오류 표출 후 재입력을 받음
                    print("Wrong input!")
            if ans=='yes': 
                continue #새로운 게임을 시작함
            else:
                break #게임을 종료함
