def main():
    while True:
        card = int(input("Credit card number: "))
        if card >= 0:
            break
    check_card = sum_mult(card) + sum_normal(card)

    if (check_card % 10) == 0:
        if first_digit(card) == 34 or first_digit(card) == 37:
            if card_lenght(card) == 15:
                print("AMEX")
            else:
                print("INVALID")


        elif first_digit(card) > 50 and first_digit(card) < 56:
            if card_lenght(card) == 16:
                print("MASTERCARD")
            else:
                print("INVALID")


        elif first_digit(card) // 10 == 4:
            if card_lenght(card) == 13 or card_lenght(card) == 16:
                print("VISA")
            else:
                print("INVALID")
        else:
            print("INVALID")
    else:
        print("INVALID")

def card_lenght(card):
    card_lenght = 0

    while card > 0:
        card = card // 10
        card_lenght += 1

    return card_lenght

def first_digit(card):
    first_digit = 0

    while (card // 100) > 0:
        card = card // 10
        first_digit = card

    return first_digit

def sum_mult(card):
    sum_mult = 0

    while card > 0:
        num_mult(card)
        sum_mult = sum_mult + num_mult(card)
        card = card // 100

    return sum_mult

def num_mult(card):
    card = card // 10
    num_mult = (card % 10) * 2

    if (num_mult // 10) > 0:
        num_mult = (num_mult % 10) + (num_mult // 10)
    card = card // 100

    return num_mult

def sum_normal(card):
    sum_normal = 0

    while card > 0:
        sum_normal = sum_normal + (card % 10)
        card = card // 100

    return sum_normal

main()