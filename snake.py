import curses
import random
import time
from curses import wrapper

#Setup curses: 
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
width = 35
height = 25
#Create new window for game
win = curses.newwin(height,width,0,0)
win.border()
#Wait 100ms between refresh
win.timeout(100)
#Borders: If snake is in the border, the game is lost
bordersy = [0,height-1]
bordersx = [0,width-1] 


def play(win):
    #Instantiate snake and food:
    mysnake = snake(10,10,win)
    snakefood = food(mysnake,win)
    acceptedkeys = [ord('w'),ord('a'),ord('s'),ord('d'),-1]
    #Begin while loop:
    while True:
        head = mysnake.parts[0]    
        keyinput = win.getch() #Key input as ASCII int. If key is not wasd or there is no input, input is set to -1. win.getch() automatically returns -1 if there is no input.
        if keyinput not in acceptedkeys:
            keyinput = -1
        #snake movement direction is updated, and snake is moved. Food instance is passed to move method.
        mysnake.direction = mysnake.direction if keyinput == -1 else chr(keyinput)
        mysnake.move(snakefood)

class food():
    def __init__(self,mysnake,win):
        self.reset(mysnake,win)

    #reset creates a new location for the food, and prints food in the window.
    def reset(self,mysnake,win):
        self.location = None
        while self.location == None:
            y,x = random.randint(1,height-2), random.randint(1,width-2)
            #If food is inside the snake, a new food location is generated.
            if [y,x] not in mysnake.parts:
                self.location = [y,x]
        self.win = win
        win.addch(self.location[0],self.location[1],'O')

class snake():
    def __init__(self,ypos,xpos,win):
        self.parts = [[ypos,xpos],[ypos,xpos-1],[ypos,xpos-2]] #The individual coordinates of the snake body
        self.direction = 'd' #Direction that the snake is moving in
        self.win = win 
        for list in self.parts:
            win.addch(list[0],list[1],'X')

    def move(self,snakefood):
        head = self.parts[0]
        #Check if game has been lost:
        if head[0] in bordersy or head[1] in bordersx:
            self.losegame()
        if head in self.parts[1:]:
            self.losegame()
        #Insert part in the new direction of movement
        if self.direction == 'd':
            self.parts.insert(0,[head[0],head[1]+1])
        if self.direction == 'a':
            self.parts.insert(0,[head[0],head[1]-1])
        if self.direction == 'w':
            self.parts.insert(0,[head[0]-1,head[1]])
        if self.direction == 's':
            self.parts.insert(0,[head[0]+1,head[1]])
        if head == snakefood.location:
            self.eat(snakefood)
        else:
            #Tail of snake is removed, so the total length of the snake remains the same until snake reaches food and eat() is called
            oldtail = self.parts.pop()
            self.win.addch(int(self.parts[0][0]),int(self.parts[0][1]),'X')
            self.win.addch(oldtail[0],oldtail[1],' ')
        return

    def eat(self,snakefood):
        self.win.addch(int(self.parts[0][0]),int(self.parts[0][1]),'X')
        snakefood.reset(self,win)

    def losegame(self):
        #Game is lost. Window gets ended, and the score (total length of snake) is printed.
        curses.endwin()
        print('You lose. Score: {!s}'.format(str(len(self.parts))))
        time.sleep(3)
        quit()

if __name__ == '__main__':
    wrapper(play(win))
