while True:
    text = str(input("Text: "))

    count_letters = 0
    count_words = 1
    count_sentences = 0

    if(text):
        for i in range(len(text)):
            if (text[i].isalpha()):
                count_letters += 1

            elif (text[i].isspace()):
                count_words += 1

            elif (text[i] == '!' or text[i] == '.' or text[i] == '?'):
                count_sentences += 1

        L = float(count_letters / count_words * 100)
        S = float(count_sentences / count_words * 100)
        formula = round((float)(0.0588 * L - 0.296 * S - 15.8))

        if formula < 1:
            print("Before Grade 1")

        elif formula >= 16:
            print("Grade 16+")

        else:
            print(f"Grade {formula}")

        break