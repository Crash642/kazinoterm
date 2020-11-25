from ctypes import *
import time
import random

valuta = "руб"
money = 0
playGame = True
startMoney = 0
defaulMoney = 10000
windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

#Чтение из файла оставшейся суммы
def Loadmoney():
    try:
        f = open("money.dat", "r")
        m = int(f.readline())
        f.close()
    except FileNotFoundError:
        print(f"Файла не существует, задано значение {defaulMoney} {valuta}")
        m = defaulMoney
    return m

#Запись суммы в файле
def saveMoney(moneyToSave):
    try:
        f = open("money.dat", "w")
        f.write(str(moneyToSave))
        f.close()
    except:
        print("Ошибка создания файла, наше Казино закрывается!")
        quit(0)

#Установка цвета текста
def color(c):
    windll.Kernel32.SetConsoleTextAttribute(h, c)

# ВЫвод на экран цветного обрамленного звездочками текста
def colorLine(c, s):
    color(c)
    print("*" * (len(s) + 2))
    print(" " + s)
    print("*" * (len(s) + 2))

#Функция ввода целого числа
def getIntInput(minimum, maximum, message):
    color(7)
    ret = -1
    while (ret < minimum or ret > maximum):
        st = input(message)
        if (st.isdigit()):
            ret = int(st)
        else:
            print('     Введите целое число!')
        return ret

#Функция ввода значений 
def getInput(digit, message):
    color(7)
    ret = ""
    while (ret == "" or not ret in digit):
        ret = input(message)
    return ret

#Вывод сообщения о выйгрыше
def pobeda(resuilt):
    color(14)
    print(f"    Победа за тобой! Выйгрыш составил: {resuilt} {valuta}")
    print(f"    У тебя на счету: {money}")

#Вывод сообщения о пройгрыше
def proigt(result):
    color(12)
    print(f"    К сожалению, проигрыш: {result} {valuta}")
    print(f"    У тебя на счету: {money}")
    print("     Обязательно нужно отыграться!")

# Однорукий бандит 
def getMaxCount(digit, v1, v2, v3, v4, v5):
    ret = 0
    if digit == v1:
        ret += 1
    if digit == v2:
        ret += 1
    if digit == v3:
        ret += 1
    if digit == v4:
        ret += 1
    if digit == v5:
        ret += 1

    return ret
# Однорукий Бандит
def getOHBRes(stavka):
    res = stavka
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0

    getD1 = True
    getD2 = True
    getD3 = True
    getD4 = True
    getD5 = True
    col = 10

    while(getD2 or getD1 or getD4 or getD4 or getD5):
        if (getD1):
            d1 +=1
        if (getD2):
            d2 -=1
        if (getD3):
            d3 +=1
        if (getD4):
            d4 -=1
        if (getD5):
            d5 +=1

        if d1 > 9:
            d1 = 0
        if d2 < 0:
            d2 = 9
        if d3 > 9:
            d3 = 0
        if d4 < 0:
            d4 = 9
        if d5 > 9:
            d5 = 0

        if random.randint(0, 20) == 1:
            getD1 = False
        if random.randint(0, 20) == 1:
            getD2 = False
        if random.randint(0, 20) == 1:
            getD3 = False
        if random.randint(0, 20) == 1:
            getD4 = False
        if random.randint(0, 20) == 1:
            getD5 = False

        time.sleep(0.1)
        color(col)
        col += 1
        if (col > 15):
            col = 10

        print('     ' + "%" * 10)
        print(f"     {d1} {d2} {d3} {d4} {d5}")
    
    maxCount = getMaxCount(d1, d1, d2, d3, d4, d5)
    if (maxCount < getMaxCount( d2, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount( d2, d1, d2, d3, d4, d5)
    if (maxCount < getMaxCount( d3, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount( d3, d1, d2, d3, d4, d5)    
    if (maxCount < getMaxCount( d4, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount( d4, d1, d2, d3, d4, d5)
    if (maxCount < getMaxCount( d5, d1, d2, d3, d4, d5)):
        maxCount = getMaxCount( d5, d1, d2, d3, d4, d5)
    
    color(14)
    if (maxCount == 2):
        print(f" Совпадение двух чисел! Твой выйгрыш в размере ставки: {res}")
    elif (maxCount == 3):
        res *= 2
        print(f" Совпадение трех чисел! Твой выйгрыш 2:1: {res}")
    elif (maxCount == 4):
        res *= 5
        print(f" Совпадение ЧЕТЫРЕХ чисел! Твой выйгрыш 5:1: {res}")
    elif (maxCount == 5):
        res *= 10
        print(f" БИНГО! Совпадение всех чисел! Твой выйгрыш 10:1: {res}")
    else:
        proigt(res)
        res = 0

    color(11)
    print()
    input("Нажмите ENTER для продолжения...")
    return res
#Алгоритм игры однорукий бандит
def oneHandBandit():
    global money
    playGame = True
    while (playGame):
        colorLine(3, "ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В ОДНОРУКОГО БАНДИТА!")
        color(14)
        print(f"\n У тебя на счету {money} {valuta}\n")
        color(5)
        print('ПРАВИЛА ИГРЫ ...')
        print("     1.При совпадение 2-х чисел ставка не списывается")
        print("     2.При совпадение 3-х чисел выйгрыш 2:1)")
        print("     3.При совпадение 4-х чисел выйгрыш 5:1")
        print("     4.При совпадение 5-х чисел выйгрыш 10:1")
        print("     5.Ставка 0 для завершения игры\n")

        stavka = getIntInput(0, money, f"   Введите ставку от 0 до {money}: ")
        if stavka == 0:
            return 0

        money -= stavka
        money += getOHBRes(stavka)

        if (money <= 0):
            playGame = False

#Рулетка визуал
def getRoulette(visible):
    tickTime = random.randint(100, 200) / 10000
    mainTime = 0
    number = random.randint(0, 38)
    increaseTickTime = random.randint(100, 110) / 100
    col = 1

    while (mainTime < 0.7):
        col += 1
        if col > 15:
            col = 1

        mainTime += tickTime
        tickTime *= increaseTickTime

        color(col)
        number += 1
        if (number > 38):
            number = 0
            print()

        printNumber = number
        if (number == 37):
            printNumber = "00"
        elif (number == 38):
            printNumber = "000"
        
        print("Число >",
            printNumber,
            "*" * number,
            " " * (79 - number * 2),
            "*" * number)
        if (visible):
            time.sleep(mainTime)
    return number
# Сам алгоритм игры рулетка
def roulette():
    global money
    playGame = True

    while (playGame and money > 0):
        colorLine(3, "ДОБРО ПОЖАЛОВАТЬ НА ИГРУ В РУЛЕТКУ!")
        color(14)
        print(f"\n У тебя на счету {money} {valuta}\n")
        color(11)
        print('Ставлю на ...')
        print("     1.Четное(выйгрыш 1:1)")
        print("     2.Нечетное(выйгрыш 1:1)")
        print("     3.Дюжина(выйгрыш 3:1)")
        print("     4.Число(выйгрыш 36:1)")
        print("     0.Возврат в предыдущее меню")

        x = getInput("01234", "     Твой выбор? ")

        playRoulette = True
        if (x == "3"):
            color(2)
            print()
            print("Выбери числа:...")
            print("     1. От 1 до 12")
            print("     2. От 13 до 24")
            print("     3. От 25 до 36")
            print("     0. Назад")

            duzhina = getInput("01234", "      Твой выбор?")
            if (duzhina == "1"):
                textDruzhina = "От 1 до 12"
            elif (duzhina == "2"):
                textDruzhina = "От 13 до 24"
            elif (duzhina == '3'):
                textDruzhina = "От 25 до 36"
            elif duzhina == "0":
                playRoulette = False
        elif (x == "4"):
            chislo = getIntInput(0,36, "   На какое число ставишь? (0..36): ")
        
        color(7)
        if (x == "0"):
            return 0
        
        if (playRoulette):
            stavka = getIntInput(0, money, f"   Сколько поставишь? (не больше {money}):")
            if (stavka == 0):
                return 0
            
            number = getRoulette(True)

            print()
            color(11)
            if (number < 37):
                print(f"    Выпало число {number}! " + "*" * number)
            else:
                if (number == 37):
                    printNumner = "00"
                elif (number == 38):
                    printNumner = "000"
                print(f"    Выпало число {printNumner}!")

            if (x == "1"):
                print("     Ты ставил на ЧЕТНОЕ!")
                if (number < 37 and number % 2 == 0):
                    money += stavka
                    pobeda(stavka)
                else:
                    money -= stavka
                    proigt(stavka)
            elif (x == "2"):
                print("     Ты ставил на НЕЧЕТНОЕ!")
                if (number < 37 and number % 2 != 0):
                    money += stavka
                    pobeda(stavka)
                else:
                    money -= stavka
                    proigt(stavka)
            elif (x == "3"):
                print(f"       Ставка сделанна на диапазон чисел {textDruzhina}.")
                winDruzhina = ""
                if (0 < number < 13):
                    winDruzhina = "1"
                elif (12 < number < 25):
                    winDruzhina = "2"
                elif (24 < number < 37):
                    winDruzhina = "3"
                
                if (duzhina == winDruzhina):
                    money += stavka * 2
                    pobeda(stavka * 3)
                else:
                    money -= stavka
                    proigt(stavka)
            elif (x == "4"):
                print(f"    Ставка сделанна на число {chislo}")
                if (number == chislo):
                    money += stavka * 35
                    pobeda(stavka * 36)
                else:
                    money -= stavka
                    proigt(stavka)
            
            print()
            input("Нажмите ENTER для продолжения...")

#Анимация костей
def getDice():
    count = random.randint(3, 8)
    sleep = 0
    while (count > 0):
        color(count + 7)
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        print(" " * 10, "----- -----")
        print(" " * 10, f"| {x} | | {y} |")
        print(" " * 10, "----- -----")
        time.sleep(sleep)
        sleep += 1 / count
        count -= 1
    return x + y
#Кости
def dice():
    global money
    playGame = True

    while(playGame):

        print()
        colorLine(3, "ДОБРО ПОЖАЛОВАТЬ НА ИГРУ КОСТИ!")
        color(14)
        print(f"\n У  тебя на счету {money} {valuta}\n")

        color(7)
        stavka = getIntInput(0, money, f"   Сделай ставку в пределах {money} {valuta} ")
        if stavka == 0:
            return 0
        
        playRound = True
        control = stavka
        oldResult = getDice()
        firstPlay = True

        while (playRound and stavka > 0 and money > 0):
            if (stavka > money):
                stavka = money
            
            color(11)
            print(f"\n      В твоем распоряжение {stavka} {valuta}")
            color(12)
            print(f"\n      Текущая сумма чисел на костях: {oldResult}")
            color(11)
            print("\n Сумма чисел на гранях будет больше, меньше или равна предыдущей?")
            color(7)
            x = getInput("0123", "  Введи 1 - больше, 2 - меньше, 3 - равно или 0 - выход: ")
            if (x != "0"):
                firstPlay = False
                if(stavka > money):
                    stavka = money

                money -= stavka
                diceResult = getDice()

                win = False
                if (oldResult > diceResult):
                    if (x == "2"):
                        win = True
                elif (oldResult < diceResult):
                    if (x == "1"):
                        win = True

                if (not x == "3"):
                    if (win):
                        money += stavka + stavka // 5
                        pobeda(stavka // 5)
                        stavka += stavka // 5
                    else:
                        stavka = control
                        proigt(stavka)
                elif x  == 3:
                    if (oldResult == diceResult):
                        money += stavka * 3
                        pobeda(stavka * 3)
                        stavka *= 3
                    else:
                        stavka = control
                        proigt(stavka)
                oldResult = diceResult
            else:
                if(firstPlay):
                    money -= stavka
                playRound = False

#Запуск игры
def main():
    global money, playGame
    
    money = Loadmoney()
    startMoney = money

    while (playGame and money > 0):
        colorLine(10, "Приветствую тебя в нашем казино, дружище!")
        color(14)
        print(f"У тебя на счету {money} {valuta}")

        color(6)
        print("Ты можешь сыграть в:")
        print("     1. Рулетку")
        print("     2. Кости")
        print("     3. Однорукого Бандита")
        print("     0. Выход. Ставка 0 в играх - выход.")
        color(7)

        x = getInput("01234", "     Твой выбор?")

        if (x == "0"):
            playGame = False
        elif (x == "1"):
            roulette()
        elif (x == "2"):
            dice()
        elif (x == "3"):
            oneHandBandit()
    colorLine(12, "Жаль, что ты покидаешь нас! Но возвращайся скорее!")
    color(13)
    if (money < 0):
        print("Упс, ты остался без денег! Приходи когда будут ещё!")
    color(11)
    if (money > startMoney):
        print("Ну чтож, поздравляем с прибылью!")
        print(f"На начало игры у тебя было {startMoney} {valuta}")
        print(f"Сейчас уже {money} {valuta}! Играй ещё и приумножай!")
    elif (money == startMoney):
        print("Ты ничего не выйграл и не приумножил! Заходи ещё!")
    else:
        print(f"К сожалению, ты проиграл {startMoney - money} {valuta}")
        print("в следующий раз все обязательно получится!")
    saveMoney(money)

    color(7)
    quit(0)
main()   
