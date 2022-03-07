import random

#which fields have which character (x, o, or none)
belegung = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

#situations in that one player wins, each field has a numbers
wins = [[0,4,8],[2,4,6],[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8]]

#function that returns the grid and the chars as string
def spielfeld():
    return belegung[0] + ' | ' + belegung[1] + ' | ' + belegung[2] + '\n---------\n' + belegung[3] + ' | ' + belegung[4] + ' | ' + belegung[5] + '\n---------\n' + belegung[6] + ' | ' + belegung[7] + ' | ' + belegung[8]

#check if someone won and check who won
def get_if_won():
    won = False
    winner = ''
    for i in range(len(wins)):
        if belegung[wins[i][0]] == belegung[wins[i][1]] == belegung[wins[i][2]] and belegung[wins[i][0]] != ' ':
            won = True
            winner = belegung[wins[i][2]]
            break
    return [won , winner]

#check if the bot has the chance to win
def get_if_self_close():
    self_close = False
    self_close_case = wins[0]
    self_close_case_int = 100
    for i in range(len(wins)):
        if belegung[wins[i][0]] == belegung[wins[i][1]] == 'o' != ' ' and belegung[wins[i][2]] == ' ':
            self_close = True
            self_close_case = wins[i]
            self_close_case_int = 2
            break
        elif belegung[wins[i][0]] == belegung[wins[i][2]] == 'o' != ' ' and belegung[wins[i][1]] == ' ':
            self_close = True
            self_close_case = wins[i]
            self_close_case_int = 1
            break
        elif belegung[wins[i][1]] == belegung[wins[i][2]] == 'o' != ' ' and belegung[wins[i][0]] == ' ':
            self_close = True
            self_close_case = wins[i]
            self_close_case_int = 0
            break
    return [self_close , self_close_case , self_close_case_int]

#check if the player has the chance to win
def get_if_close():
    close = False
    close_case = wins[0]
    close_case_int = 100
    for i in range(len(wins)):
        if belegung[wins[i][0]] == belegung[wins[i][1]] != ' ' and belegung[wins[i][2]] == ' ':
            close = True
            close_case = wins[i]
            close_case_int = 2
            break
        elif belegung[wins[i][0]] == belegung[wins[i][2]] != ' ' and belegung[wins[i][1]] == ' ':
            close = True
            close_case = wins[i]
            close_case_int = 1
            break
        elif belegung[wins[i][1]] == belegung[wins[i][2]] != ' ' and belegung[wins[i][0]] == ' ':
            close = True
            close_case = wins[i]
            close_case_int = 0
            break
    return [close , close_case , close_case_int]

def get_num_of_close(char):
    close_am = 0
    close_cases = []

    for i in range(len(wins)):

        if belegung[wins[i][0]] == belegung[wins[i][1]] == char != ' ' and belegung[wins[i][2]] == ' ':
            close_am += 1
            close_cases.append(wins[i])

        elif belegung[wins[i][0]] == belegung[wins[i][2]] == char != ' ' and belegung[wins[i][1]] == ' ':
            close_am += 1
            close_cases.append(wins[i])

        elif belegung[wins[i][1]] == belegung[wins[i][2]] ==  char != ' ' and belegung[wins[i][0]] == ' ':
            close_am += 1
            close_cases.append(wins[i])

    #print(close_am,close_cases)
    return [close_am,close_cases]

def get_if_possible_dilemma(char):
    is_close = False
    critical_char = 100
    found = False
    twice = False

    for i in range(9):
        if belegung[i] == ' ':
            belegung[i] = char

            if get_num_of_close(char)[0] > 1:
                is_close = True

                for k in range(3):
                    for j in range(3):
                        if get_num_of_close(char)[1][0][k] == get_num_of_close(char)[1][1][j]:
                            critical_char = get_num_of_close(char)[1][1][j]
                            found = True
                            break
                    
                    if found:
                        break

                belegung[critical_char] = 'o'

                if get_if_possible_dilemma('x')[0]:
                    print('blbalblablalbl')
                    twice = True
                    break

                belegung[critical_char] = ' '

            belegung[i] = ' '
    return [is_close, critical_char,twice]

def get_if_can_create_must():
    
    possible = False
    field = 100

    for i in range(9):

        if belegung[i] == ' ':
            belegung[i] = 'o'

            

            belegung[i] = ' '

    return [possible, field]

#get free fields and free corners (bot preferbly sets o's in corners)
def get_free_fields():
    corners = [0,2,6,8]
    free_fields = []
    free_corners = []

    for i in range(len(belegung)):
        if belegung[i] == ' ':
            free_fields.append(i)
    
    for i in range(len(corners)):
        if belegung[corners[i]] == ' ':
            free_corners.append(corners[i])
    
    return [free_fields,free_corners]

#this is the bot setting his o
def set_o():
    #only act if there are free fields
    if len(get_free_fields()[0]) != 0:

        #check if the bot has the chance to win and set the o
        if get_if_self_close()[0]:
            print('self close')
            belegung[get_if_self_close()[1][get_if_self_close()[2]]] = 'o'

        #check if the player has the chance to win and set the o
        elif get_if_close()[0]:
            print('close')
            belegung[get_if_close()[1][get_if_close()[2]]] = 'o'

        #check if the bot can create a dilemma
        elif get_if_possible_dilemma('o')[0]:
            print('can create dilemma')
            belegung[get_if_possible_dilemma('o')[1]] = 'o'

        #check if the bot can create a must
        elif get_if_can_create_must()[0]:
            print('can create must')
            belegung[get_if_can_create_must()[1]] = 'o'

        #check if there might be a dilemma incoming
        elif get_if_possible_dilemma('x')[0]:
            print('avoid dilemma')
            belegung[get_if_possible_dilemma('x')[1]] = 'o'

        #check if the middle field is free and set the o
        elif belegung[4] == ' ':
            print('set middle')
            belegung[4] = 'o'
        
        #check if corners are free, if yes, set o to a random corner
        elif len(get_free_fields()[1]) > 0:
            print('set corner')
            belegung[get_free_fields()[1][random.randint(0,len(get_free_fields()[1])-1)]] = 'o'

        #otherwise just set randomly somewhere
        else:
            print('random')
            belegung[get_free_fields()[0][random.randint(0,len(get_free_fields()[0])-1)]] = 'o'

#get user input and set x on the position (1-9) the player typed
def get_input():

    pos = int(input('Set x at: ')) - 1
    if pos >= len(belegung) or pos < 0 or belegung[pos] != ' ':
        print('This field is already set or out of range')
        get_input()
    else:
        belegung[pos] = 'x'    

#print grid at the beginning of the game
print(spielfeld())

#while nobody has won, repeat getting input and setting o's
while not get_if_won()[0]:
    get_input()
    if not get_if_won()[0]:
        set_o()
        print(spielfeld())
    #check if there is a tie
    tie = True
    for i in range(len(belegung)):
        if belegung[i] == ' ':
            tie = False
            break
    if tie:
        print('That\'s a tie!')
        break

#print the winner once someone won
while get_if_won()[0]:
        if get_if_won()[1] == 'x':
            print(spielfeld())
            print('You won!')
            break
        elif get_if_won()[1] == 'o':
            print('I won!')
            break

input('Press enter to close')