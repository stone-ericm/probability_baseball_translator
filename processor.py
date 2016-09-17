from app import situation
import csv
import re
import os

prog = re.compile('^(\d|HR|K|NP|S|D|T|IW|W|E|SB|C|FC|OA|PO|POCS|FLE|BK|PC|WP|HP|CS|DI|PB)')

def report_error(filename, play):
    with open('error.txt', 'a') as error:
        error.write(filename+'\n')
        error.write(play+'\n')

def base_check(play):
    if '.' in play:
        #print(game_sit)
        # THIS CAN BE USED MORE GENERALLY
        # EVALUATE B-1 LAST
        
        if '3-H' in play:
            game_sit['3rd'] = False
            game_sit['net_score'] += 1
            #print(game_sit)
        elif '3XH' in play:
            game_sit['outs'] += 1
            game_sit['3rd'] = False
            #print(game_sit)
        if '2-3' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = True
            #print(game_sit)
        elif '2X3' in play:
            game_sit['outs'] += 1
            game_sit['2nd'] = False
            #print(game_sit)
        if '2-H' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['net_score'] += 1
            #print(game_sit)
        elif '2XH' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['outs'] += 1
            #print(game_sit)
        if '1-2' in play:
            game_sit['1st'] = False
            game_sit['2nd'] = True
            #print(game_sit)
        elif '1X2' in play:
            game_sit['1st'] = False
            game_sit['outs'] += 1
            #print(game_sit)
        if '1-3' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = True
            game_sit['1st'] = False
            #print(game_sit)
        elif '1X3' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['outs'] += 1
            #print(game_sit)
        if '1-H' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['net_score'] += 1
            #print(game_sit)
        elif '1XH' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['outs'] += 1
            #print(game_sit)
        if 'B-1' in play:
            game_sit['1st'] = True
        elif 'BX1' in play:
            game_sit['outs'] += 1
        if 'B-2' in play:
            game_sit['2nd'] = True
            game_sit['1st'] = False
        elif 'BX2' in play:
            game_sit['2nd'] = False
            game_sit['1st'] = False
            game_sit['outs'] += 1
        if 'B-3' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = True
            game_sit['1st'] = False
        elif 'BX3' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['outs'] += 1
        if 'B-H' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['net_score'] += 1
        elif 'BXH' in play:
            game_sit['2nd'] = False
            game_sit['3rd'] = False
            game_sit['1st'] = False
            game_sit['outs'] += 1

def event_check(play):
    # print(game_sit['outs'])
    # print(play[0].isdigit())
    if prog.search(play):
        #EVENT TYPES
        
        if play[0].isdigit():
            game_sit['outs'] += 1
            # if '.' in play:
            base_check(play)
            #print(game_sit)
                
                # exit()
        #Wild Pitch, Passed Ball, Balk, Defensive Indifference, Other
        elif play[0:2] in ['WP', 'PB', 'BK', 'DI', 'OA']:
            base_check(play)
            #print(game_sit)
        
        #Hit by pitch, Intentional Walk, Walk, Error (allowing a batter to get on base)
        elif play[0:2] in ['HP', 'IW'] or play[0] in ['W', 'E']:
            base_check(play)
            game_sit['1st'] = True
            #print(game_sit)
        
        #Strikeout
        
        elif play[0] == 'K':
            # if len(play) == 1:
            try:
                if play[1] == '+':
                    if play[2:4] in ['WP', 'PB']:
                        base_check(play)
                    elif play[2] == 'E':
                        base_check(play)
            # else:
            except IndexError:
                game_sit['outs'] += 1
                base_check(play)
        
        #Caught Stealing
        
        elif play[0:2] == 'CS':
            if play[2] == '2':
                game_sit['1st'] = False
            elif play[2] == '3':
                game_sit['2nd'] = False
            elif play[2] == 'H':
                game_sit['3rd'] = False
            game_sit['outs'] += 1
            base_check(play)
        
        #Foul Error
        elif play[0:3] == 'FLE' or play[0:2] == 'NP':
            pass
        
        elif play[0:2] == 'PO':
            if play[2:4] == "CS":
                if play[4] == '1':
                    game_sit['1st'] = False
                elif play[4] == '2':
                    game_sit['2nd'] = False
                elif play[4] == '3':
                    game_sit['3rd'] = False
            else:
                if play[2] == '1':
                    game_sit['1st'] = False
                elif play[2] == '2':
                    game_sit['2nd'] = False
                elif play[2] == '3':
                    game_sit['3rd'] = False
            game_sit['outs'] += 1
            base_check(play)
        
        elif play[0] in ['C', 'S']:
            if 'B-' not in play:
                play = play + 'B-1'
            base_check(play)
        
        elif play[0:2] == 'FC':
            base_check(play)
        
        elif play[0:2] == 'SB':
            if 'SB2' in play:
                play = play + '.1-2'
            if 'SB3' in play:
                play = play + '2-3'
            if 'SBH' in play:
                play = play + '3-H'
            base_check(play)
        
        elif 'DP' in play:
            if play[play.index('(')+1] == '1':
                play = play + '1X2'
            if play[play.index('(')+1] == '2':
                play = play + '2X3'
            if play[play.index('(')+1] == '3':
                play = play + '3XH'
            play = play + 'BX1'
            base_check(play)
            
        elif 'TP' in play:
            game_sit['outs'] = 3
            
        elif play[0] == 'D':
            if 'B-' not in play:
                play = play + 'B-2'
            base_check(play)
        
        elif play[0] == 'T':
            if 'B-' not in play:
                play = play + 'B-3'
            base_check(play)
        

        # else:
        #     report_error(filename, play)
    else:
        report_error(filename, play)

for filename in os.listdir('evx'): 
    with open('evx/' + filename) as csvfile:
        print(filename)
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'info' and row[1] == 'date':
                print(row[2])
            if row[0] == 'start':
                try:
                    if game_sit['inning'] != 1:
                        # print(game_sit)
                        exit()
                except NameError:
                    game_sit = {
                        'inning': 1,
                        'team': 0,
                        'outs': 0,
                        # 'base_sit': 1,
                        '1st': False,
                        '2nd': False,
                        '3rd': False,
                        'net_score': 0
                    }
            if row[0] == "play":
                play = row[6]
                print(play)
                event_check(play)
                print(game_sit)
                
                    ##CHECK NUMBER OF OUTS
                if game_sit['outs'] > 2:
                    game_sit['inning'] += 0.5
                    if game_sit['inning']%1 == 0:
                        game_sit['team'] = 0
                    else:
                        game_sit['team'] = 1
                    game_sit['outs'] = 0
                    game_sit['1st'] = False
                    game_sit['2nd'] = False
                    game_sit['3rd'] = False
                    game_sit['net_score'] = -game_sit['net_score']
    exit()
                    # print('yeah')
                # else:

            # if row[6][0] not in ['K', 'N', 'H', 'S', 'D', 'T', 'I', 'W', 'E', 'C']:
            #     if not row[6][0].isdigit():
            #         print (row[6])
            # if '.' in row[6]:
            #     row[6].index('.')
            #     movement = row[6][3:]
            #     if 
            # if row[6][0] in ['S', 'D', 'T', 'H', ]