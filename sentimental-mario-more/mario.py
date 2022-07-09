
while True:
    height = int(input("Height: "))
    lenght = 1
    space = height - 1

    if height < 1 or height > 8:
        print("Invalid Height")

    else:
        for i in range(height):
            #print left side
            print(" " * space, end="")
            #print blank spaces on left side
            print("#" * lenght, end="")
            #space on mid
            print("  ", end="")
            #print right side
            print("#" * lenght)
            #adjust counters for the loop
            lenght += 1
            space -= 1
        break
