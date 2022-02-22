
import random

file = open('/Users/claire/Projects/Wordle-Solver/wordlist.txt', 'r')
content = file.read()
word_list = content.split(",")


def letter_frequency():
    letter_frequency = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0,'h':0, 'i':0, 'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    for word in word_list:
        for letter in word:
            if letter.isalpha():
                freq = letter_frequency[letter] + 1
                letter_frequency.update({letter: freq})

    return letter_frequency

def select_word():
    all_freqs = letter_frequency()
    max_freq = max(all_freqs, key=lambda x:all_freqs[x])

    while True:
        word = random.choice(word_list)
        if(max_freq in word):
            print(word)
            break

    print(max_freq)

select_word()




