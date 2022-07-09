import csv
import sys


def main():

    STRs = []
    id = []

    # TODO: Check for command-line usage OK
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as database:
        reader = csv.DictReader(database)
        STRs = reader.fieldnames[1:]
        for row in reader:
            id.append(row)

    #The fromkeys() method creates a new dictionary from the given sequence of elements with a value provided by STRs, https://www.programiz.com/python-programming/methods/dictionary/fromkeys
    str_count = dict.fromkeys(STRs, 0)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        #The readline() method returns one line from the file.
        sequence = file.readline()

    # TODO: Find longest match of each STR in DNA sequence
        for STR in STRs:
            #from def longest_match
            str_count[STR] = longest_match(sequence, STR)


    # TODO: Check database for matching profiles
    for profile_id in id:
        match_found = 0

        for STR in STRs:
            if int(profile_id[STR]) != str_count[STR]:
                continue
            match_found += 1

        if match_found == len(STRs):
            print(profile_id['name'])
            exit(0)


    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()