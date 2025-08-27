import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) == 3:  # ch

        # TODO: Read database file into a variable
        with open(sys.argv[1], "r") as csvfile:
            reader = csv.DictReader(csvfile)

        # TODO: Read DNA sequence file into a variable
            with open(sys.argv[2], "r") as seqfile:
                sequence = seqfile.read()

        # TODO: Find longest match of each STR in DNA sequence
                # creating dict dunamically to check for STRs not mentioned in given csv files as well
                dict = {}
                length = len(reader.fieldnames)
                # skipping through name, hence starting from 1
                for i in reader.fieldnames[1:length]:
                    dict[i] = str(longest_match(sequence, i))

        # TODO: Check database for matching profiles
                for row in reader:
                    count = 0
                    # checking for each STR
                    for STR in dict:
                        # checking for longest match between csv file and calculated one
                        if row[STR] == dict[STR]:
                            count += 1
                    if count == length - 1:
                        # printing name of person identified
                        print(row['name'])
                        break
                else:
                    print("No match")


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
