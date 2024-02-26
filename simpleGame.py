import curses
import random
import time
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
maxn = curses.LINES - 1
maxm = curses.COLS - 1

field = []
food = []
enemy = []
score = usr_i = usr_j = 0
playing = True
def rand_cell():
    x = random.randint(0, maxn)
    y = random.randint(0, maxm)
    while(field[x][y] != ' '):
        x = random.randint(0, maxn)
        y = random.randint(0, maxm)
    return x, y
    

def init():
    global usr_i, usr_j
    for i in range(-1, maxn+1):
        field.append([])
        for j in range(-1, maxm+1):
            if random.randint(0,95) == 0:
                field[i].append('.')
            else:
                field[i].append(' ')
    usr_i, usr_j = rand_cell()
    for i in range(50):
        fi, fj = rand_cell()
        ftime = random.randint(10, 10)
        food.append((fi, fj, ftime))
    for i in range(25):
        ei, ej = rand_cell()
        enemy.append((ei, ej))
    

def draw():
    for i in range(maxn):
        for j in range(maxm):
            stdscr.addch(i, j, field[i][j])
    stdscr.addch(usr_i, usr_j, '🧿')
    for i in range(len(food)):
        fi, fj, ftime = food[i]
        stdscr.addch(fi, fj, '🍕')
    for i in range(len(enemy)):
        ei, ej = enemy[i]
        stdscr.addch(ei, ej, '👹')
    
    stdscr.addstr(0, 0, f"SCORE = {score}")
    stdscr.refresh()

def move(c):
    global usr_i, usr_j, score, playing
    tmp_i = usr_i
    tmp_j = usr_j
    if c == 'a':
        tmp_j -= 1
    elif c == 's':
        tmp_i += 1
    elif c == 'd':  
        tmp_j += 1
    elif c == 'w': 
        tmp_i -= 1
    if tmp_j > 0 and tmp_j < maxm and tmp_i > 0 and tmp_i < maxn and field[tmp_i][tmp_j] != '.':
        usr_i = tmp_i
        usr_j = tmp_j
    for i in range(len(food)):
        fi, fj, ftime = food[i]
        if(usr_i == fi and usr_j == fj):
            score += 50
            fi, fj = rand_cell()
            ftime = random.randint(2000,10000)
            food[i] = (fi, fj, ftime)
            break
        else: ftime -= 1
        if ftime == 0:
            fi, fj = rand_cell()
            ftime = random.randint(2000, 10000)
            food[i] = fi, fj, ftime
    
    for i in range(len(enemy)):
        ei, ej = enemy[i]
        if random.random() < 0.005 :
            if(ei > usr_i): ei += random.choice([-1,0])
            else: ei += random.choice([1,0])
            if(ej > usr_j): ej += random.choice([-1,0])
            else: ej += random.choice([1,0])
            ei += random.choice([-1,0,1])
            ej += random.choice([-1,0,1])
            if ei > -1 and ei < maxn and ej > -1 and ej < maxm : 
                enemy[i] = ei, ej
        if(usr_i == ei and usr_j == ej):
            stdscr.addstr(maxn//2, maxm//2, "GAME OVER!")
            stdscr.refresh()
            time.sleep(5)
            playing = False        

init()

while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ''
    if c in 'asdw':
        move(c)
    elif c == 'q':
        playing = False
    draw()

stdscr.refresh()
curses.endwin()