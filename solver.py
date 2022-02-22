import time
import random
from numpy import correlate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


used_letters_list = []
game_won = False
count = 0

file = open('/Users/claire/Projects/Wordle-Solver/wordlist.txt', 'r')
content = file.read()
word_list = content.split(",")
remove_list =[]
letter_frequency_dict = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0,'h':0, 'i':0, 'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}


browser = webdriver.Chrome('/Users/claire/chromedriver') ## <-- Include proper path to your chrome driver
browser.get('https://www.nytimes.com/games/wordle/index.html')

shadow_root = browser.find_element(By.CSS_SELECTOR, 'game-app').shadow_root

game = shadow_root.find_element(By.CSS_SELECTOR, '#game')
game.click()

def remove_letter(letter):
    letter_frequency_dict.pop(letter)
    for word in word_list[:]:
        if(letter in word):
            word_list.remove(word)

def require_words_correct_letter(letter, ind):
    for word in word_list[:]:
        if(word[ind] != letter):
            word_list.remove(word)

def require_words_used_letter():
    for word in word_list[:]:
        for letter in used_letters_list:
            if(letter not in word):
                word_list.remove(word)

def check_result():
    host = browser.find_element(By.CSS_SELECTOR, "game-app")
    
    for i in range(6):
        absent = browser.execute_script("return arguments[0].shadowRoot.querySelector('#board  game-row:nth-of-type({})').shadowRoot.querySelector('game-tile[evaluation=absent]:nth-of-type({})')".format(count + 1, i), host)
        present = browser.execute_script("return arguments[0].shadowRoot.querySelector('#board  game-row:nth-of-type({})').shadowRoot.querySelector('game-tile[evaluation=present]:nth-of-type({})')".format(count + 1, i), host)
        correct = browser.execute_script("return arguments[0].shadowRoot.querySelector('#board  game-row:nth-of-type({})').shadowRoot.querySelector('game-tile[evaluation=correct]:nth-of-type({})')".format(count + 1, i), host)
        if(correct != None):
            letter = word[i]
            used_letters_list.append(letter)
            require_words_correct_letter(letter, i)

        if(present != None):
            letter = word[i]
            used_letters_list.append(letter)
            require_words_used_letter()
           
        
        if(absent != None):
            letter = word[i]
            if(letter not in used_letters_list):
                remove_letter(letter)

def letter_frequency():
    for word in word_list:
        for letter in word:
            if letter.isalpha():
                freq = letter_frequency_dict[letter] + 1
                letter_frequency_dict.update({letter: freq})
    return letter_frequency_dict

def select_word(count):
    if count == 0:
        all_freqs = letter_frequency()
        max_freq = max(all_freqs, key=lambda x:all_freqs[x])
    else:
        all_freqs = letter_frequency_dict
        max_freq = max(all_freqs, key=lambda x:all_freqs[x])
    while True:
        word = random.choice(word_list)
        if(max_freq in word):
            print(word)
            return word
    
while ~(game_won):
    
    if(count < 6):
        
        word = select_word(count)
        print("Word: " + word)
        actions = ActionChains(browser)
        actions.send_keys(word + Keys.RETURN)
        actions.perform()
        time.sleep(2)
        check_result()
        count += 1
        time.sleep(3)
    else:
        #browser.quit()
        break






