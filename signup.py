#!/bin/python
import re
import csv
from time import sleep
from datetime import datetime
from os import system

# constants

logo ='''                       _,-'``'-,_          
                   _,-'          '-,_       
               _,-'                  '-,_  
             -'                          '-
              `'-,_                  _,-'`   
                   |'-,_         _,-'|||   
                   |    '-,   ,-'    |||
           \""""\   '-,_         _,-' ''/""""/
            `\   \   _-,,'-,_,-',,-_   /   /`
              `\  \   '""'     '""'   /  /` 
                `\ \ |`````````````| / /`   
              ,-"`  \ \           / /  `"-, 
               `-.   `\`\       /`/`   .-`
                  `-.  `\`\   /`/`  .-`  
                     `-._`\`v`/`_.-`     
                         `-   -`         
               __   __ _____  _____  _____ 
              |  \_/  |_   _|/ ____|/ ____|
              | \   / | | | | (___ | |     
              | |\_/| | | |  \___ \| |     
              | |   | |_| |_ ____) | |____ 
              |_|   |_|_____|_____/ \_____|

---------------------------------------------------------'''.split('\n')

# functions

def ask(question):
    answer = input('\033[32m'+question+'\033[0m')
    return answer

def warn(warning):
    print(f"\033[31m{warning}\033[0m")

def printgreen(text):
    print('\033[32m'+text+'\033[0m')

def printlogo():
    system('clear')
    for line in logo:
        print('\033[32m'+line+'\033[0m')
    
def p(question, default='Yes'):
    while True:
        answer = ask(question)
        if not answer:
            return default
        if answer.lower() in ['y', 'yes']:
            return 'Yes'
        if answer.lower() in ['n', 'no']:
            return 'No'
        print(answer)
        warn("I didn't understand that, please type 'y' or 'n'")

# ask shit (main)

while True:
    printlogo()

    # check name
    check = True
    while check:
        name = ask("Full Name: ").split()
        alpha = True
        for part in name:
            if not part.isalpha():
                alpha = False
        if not alpha:
            warn("That doesn't look like a name, please try again.")

        else:
            if len(name) < 2:
                warn("Please enter your full name (first name and surname).")
            else:
                fname = name.pop(0)
                lname = ' '.join(name)
                check = False

    # student number
    check = True
    while check:
        snum = ask("Student Number (Press Enter if not a unimelb student): ")
        if snum.isdigit() or not snum:
            check = False
        else:
            warn("That does not look like a valid student number.")

    # email sanitisation
    invalid_email = True
    email_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    while invalid_email:
        email = ask("Email Address: ")
        if email_pattern.match(email):
            invalid_email = False
        else:
            warn('Invalid email, please try again.')

    # details if student
    course = 'NA'
    localp = 'NA'
    gradp = 'NA'
    
    if snum:
        course = ask("What course are you taking this year?: ")
        localp = p("Are you an international student? [y/N]: ", 'No')
        gradp = p("Are you a graduate student? [y/N]: ", 'No')
        
    else:
        snum = 'NA'

    # other details
    legalp = p("Are you over 18 years of age? [Y/n]: ", 'Yes')
    coolp = p("Have you used any Linux-based OS? [Y/n]: ", 'Yes')

    # pro-ness
    check = True
    while check:
        pro = ask("How much of a cyber security pro are you? (1-10): ")
        if pro.isdigit():
            pro = int(pro)
            check = False
        else:
            warn("Please enter a natural number.")
    if pro == 69:
        printgreen("Nice.")
    elif pro == 420:
        printgreen("Blaze it.")
    elif pro == 1337:
        printgreen("4w350m3.")
    elif pro > 10:
        printgreen("I like your confidence.")
    elif pro < 1:
        printgreen(":'(")

    # expectations
    expect = ask("What would you like to see from MISC in 2020?: ")
    now = datetime.now()
    time = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}"
    with open('registrations.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time, email, fname, lname, snum, course, localp, gradp, legalp, coolp, pro, 'No', expect])
        
    printgreen(f'Thank you {fname}! Welcome to MISC :)')
    sleep(3)
