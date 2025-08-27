#  input text from user
text = input("Text: ")

letter_count = 0
sent_count = 0
word_count = 1

# traversing through each character in text
for i in text:
    # if i is an alphabet, letter count is incremented
    if i.isalpha():
        letter_count += 1
    # if i is an punctiation mark ending sent, sent count is incremented
    elif i in [".", "?", "!"]:
        sent_count += 1
    # if i is an space, word count is incremented
    elif i.isspace():
        word_count += 1

# calculating average number of letters per 100 words
L = letter_count / (word_count/100)
# calculating average number of sentences per 100 words
S = sent_count / (word_count/100)

# calculating grade using Coleman-Liau index
grade = round(0.0588 * L - 0.296 * S - 15.8)

# grade conditionals
if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
