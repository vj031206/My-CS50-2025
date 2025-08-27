from cs50 import get_string


def card_check(card_num):
    sum = 0
    length = len(card_num)
    # adds digits in twice of alternating digits from second last number
    for i in range((length-2), -1, -2):
        d = int(card_num[i])*2
        for j in str(d):
            sum += int(j)
    # adds remaining digits
    for i in range((length-1), -1, -2):
        sum += int(card_num[i])
    # checks if sum ends with 0
    if sum % 10 == 0:
        return True
    else:
        return False


ccnum = get_string("Number: ")
# AMEX start with 34 or 37 - 15 digits
# MASTERCARD starts with 51,52,53,54 or 55 - 16 digits
# VISA starts with 4 - 13 or 16 digit numbers
length = len(ccnum)
if card_check(ccnum):
    #  chechikng for amex
    if length == 15 and (ccnum[0:2] == "34" or ccnum[0:2] == "37"):
        print("AMEX")
    #  checking for visa
    elif (length == 13 or length == 16) and ccnum[0] == "4":
        print("VISA")
    #  checking for mastercard
    elif length == 16 and (ccnum[0:2] in ["51", "52", "53", "54", "55"]):
        print("MASTERCARD")
    #  if neither than invalid
    else:
        print("INVALID")
# if card_check fails
else:
    print("INVALID")
