#!/bin/python
import re
import shutil
import csv
from time import sleep
from datetime import datetime
from os import system
from sys import argv

# constants

logo = '''
            _,-'``'-,_          
        _,-'          '-,_       
    _,-'                  '-,_  
  -'                          '-
   `'-,_                  _,-'`   
        |'-,_         _,-'|||   
        |    '-,   ,-'    |||
\\""""\   '-,_         _,-' ''/""""/
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

'''.split('\n')

width = int(argv[1]) if len(argv) > 1 else shutil.get_terminal_size()[0]//2

# functions

def ask(question):
    answer = input('\033[32;1m'+question+'\033[0m')
    return answer

def warn(warning):
    print(f"\033[31m{warning}\033[0m")

def printgreen(text, end='\n'):
    print('\033[32m'+text+'\033[0m', end=end)

def printline():
    print('\033[32;1m'+'-'*width+'\033[0m')

def printlogo():
    system('clear')
    k = width//2 - 17
    for line in logo:
        print('\033[32;1m'+(k*' ')+line+'\033[0m')
    printline()
    
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

def get_name():
    while True:
        name = ask("Full Name: ")
        if any([not re.match('^[a-zA-Z\-]*$', part) for part in name.split()]):
            warn("That doesn't look like a name, please try again.")
        else:
            if len(name) < 2:
                warn("Please enter your full name (first name and surname).")
            else:
                return name

def get_snum():
    while True:
        snum = ask("Student Number (Press Enter if not a unimelb student): ")
        if snum.isdigit() or not snum:
            return snum
        else:
            warn("That does not look like a valid student number.")

def get_email():
    email_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    while True:
        email = ask("Email Address: ")
        if email_pattern.match(email):
            return email
        else:
            warn('Invalid email, please try again.')

def get_course():
    course = ''
    while not course:
        course = ask("What course are you taking?: ")
        if not course:
            warn('Please enter a course (e.g. Bachelor of Science)')
    return course

def get_intl():
    return p("Are you an international student? [y/N]: ", "No")

def get_grad():
    return p("Are you a graduate student? [y/N]: ", "No")

def get_legal():
    return p("Are you over 18 years of age? [Y/n]: ", "Yes")

def get_cool():
    return p("Have you used any Linux-based OS? [Y/n]: ", "Yes")

def get_pro():
    while True:
        pro = ask("How much of a cyber security pro are you? (1-10): ")
        if pro.isdigit():
            pro = int(pro)
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
            return pro
        else:
            warn("Please enter a natural number.")

def get_comment():
    return ask("What would you like to see from MISC in 2020?: ")

# ask shit (main)

while True:
    printlogo()

    # check name
    name = get_name()

    # student number
    snum = get_snum()

    # email sanitisation
    email = get_email()

    # details if student
    course = 'NA'
    intlp = 'NA'
    gradp = 'NA'
    
    if snum:
        course = get_course()
        intlp = get_intl()
        gradp = get_grad()
        
    else:
        snum = 'NA'

    # other details
    legalp = get_legal()
    coolp = get_cool()

    # pro-ness
    pro = get_pro()

    # expectations
    expect = get_comment()

    field_names = ['Email', 'Name', 'Student Number', 'Course', 'International Student?', 'Graduate Student?', 'Over 18?', 'Linux Experience?', 'Expertise', 'Comment']
    field_vals = [email, name, snum, course, intlp, gradp, legalp, coolp, pro, expect]
    field_funcs = [get_email, get_name, get_snum, get_course, get_intl, get_grad, get_legal, get_cool, get_pro, get_comment]
    correct = False
    while not correct:
        printlogo()
        for i in range(len(field_names)):
            f = field_names[i]
            v = field_vals[i]
            printgreen(f'[{i}] {f}: ', end='')
            print(v)
        printline()
        correct = p("Are these details correct? [Y/n]: ", "Yes") == "Yes"
        if not correct:
            while True:
                inc = ask(f"Select the value you would like to change (0-{len(field_names)-1}): ")
                if inc.isdigit():
                    inc = int(inc)
                    if 0 <= inc < len(field_names):
                        field_vals[inc] = field_funcs[inc]()
                        break
                warn('Please enter a valid number.')


    now = datetime.now()
    time = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}"
    fname = field_vals[1].split().pop(0)
    lname = ' '.join(field_vals[1].split()[1:])
    out_data = [time] + [fname, lname] + field_vals[2:] + ['No'] + [field_vals[-1]]
    with open('registrations.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(out_data)
        
    printgreen(f'Thank you {fname}! Welcome to MISC :)')
    sleep(3)
