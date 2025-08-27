from cs50 import get_int
num = 0
while True:  # ifinite loop
    num = get_int("Height: ")  # input height from user
    if num > 0 and num < 9:  # checks if num between 0 and 9
        for i in range(1, num+1):
            print(" "*(num-i) + ("#"*i) + "  " + ("#"*i))
        break  # loop ends when num between 0 and 8, and half pyramid printing completed
