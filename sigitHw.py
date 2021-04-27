#1
def ex1a():
    # Function returns the sum of the input numbers
    try:
        sum = 0
        num = input("Enter a number to end stop 'stop')\n")
        while num.upper() != "STOP":
            sum += int(num)
            num = input("Enter a number to stop enter 'stop')\n")
        print(sum)
    except ValueError:
        print("Invalid input")


def ex1b():
    # Function returns the sum of the input list
    try:
        sum = 0
        list = input("Enter a list of numbers(1,4,3....)\n").split(",")
        for i in list:
            sum += int(i)
        print(sum)
    except ValueError:
        print("Invalid input")


def ex2(mat):
    # Function gets a matrix 3x3
    # Function checks if the matrix has a Tic-Tac-Toe winner and prints it
    if mat[0][0] == mat[1][1] == mat[2][2] or mat[0][0] == mat[0][1] == mat[0][2] or\
       mat[0][0] == mat[1][0] == mat[2][0]:
        print("Player", mat[0][0], "won!")
    elif mat[0][2] == mat[1][1] == mat[2][0] or \
         mat[0][2] == mat[1][2] == mat[2][2] and mat[0][2] != 0:
        print("Player", mat[0][2], "won!")
    elif mat[0][1] == mat[1][1] == mat[2][1] and mat[0][1] != 0:
        print("Player", mat[0][1], "won!")
    elif mat[1][0] == mat[1][1] == mat[1][2] and mat[1][0] != 0:
        print("Player", mat[1][0], "won!")
    elif mat[2][0] == mat[2][1] == mat[2][2] and mat[2][0] != 0:
        print("Player", mat[1][0], "won!")
    else:
        print("Tie")


def ex3(string):
    # Function gets a string
    # Function compress the string and returns it
    newString = ""
    count = 0
    if len(string) > 1:
        for i in range(len(string) - 1):
            count += 1
            if string[i] != string[i + 1]:
                newString += string[i] + str(count)
                count = 0
        if string[-2] != string[-1]:
            newString += string[-1] + str(1)
        elif string[i - 1] == string[i - 2]:
            count += 1
            newString += string[i] + str(count)
        else:
            count = 1
            newString += string[i + 1] + str(count)
    else:
        newString += string + str(1)
    return newString


def ex4(id):
    # Function gets an id
    # Function checks if the ID is valid and returns the result
    sum = 0
    toMul = 1
    if id.isdigit() and 0 < len(id) <= 9:
        for i in range(len(id) - 1):
            temp = int(id[i]) * toMul
            if temp > 9:
                temp = temp % 10 + int(temp / 10)
            sum += temp
            if toMul == 1:
                toMul = 2
            else:
                toMul = 1
        if sum % 10 != 0:
            ceiled_num = sum + (10 - sum % 10)
        else:
            ceiled_num = sum
        if ceiled_num - sum == int(id[-1]):
            return("Valid ID")
        else:
            return("Invalid ID")
    else:
        return("Invalid input")


def main():
     ex1a()
     ex1b()
     ex2([[1, 2, 0], [2, 1, 0], [2, 1, 1]])
     print(ex3("aabbbbcdddeaaaaabbcb"))
     print(ex4("543700421"))

if __name__ == "__main__":
    main()
