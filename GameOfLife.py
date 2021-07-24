import pygame, sys
import time
import random

pygame.init()

width = 400
height = 600

cells = {}
buttons = {}

FPS = 20
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")
screen.fill(pygame.Color("white"))

BASICFONTSIZE = int(width/14.4)
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

pygame.display.flip()



def main():

    defCells()
    defButtons()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Checking for mouseclicks
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked(pos)

        
        drawCells()
        drawButtons()
        drawGrid()
        pygame.display.update()
        #FPSCLOCK.tick(FPS)
    pygame.quit()
    sys.exit()


WINDOWHEIGHT = height
GRIDHEIGHT = width
GRIDWIDTH = width
numOfCells = 9
CELLSIZE = int(width/numOfCells)
BUTTONHEIGHT = GRIDWIDTH*(50/270)
BUTTONWIDTH = GRIDWIDTH*(70/270)
playButtonPos = int((GRIDWIDTH/3 - BUTTONWIDTH)/2)

def drawGrid():
    for x in range(0, GRIDWIDTH, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (x,0), (x,GRIDHEIGHT))
    for y in range(0, GRIDHEIGHT, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (0,y), (GRIDWIDTH,y))


def defCells():
    for x in range(numOfCells):
        for y in range(numOfCells):
            cells[x,y] = CellBlock(x, y, CELLSIZE)


def defButtons():
    y = 0
    for x in range(playButtonPos, GRIDWIDTH, int(GRIDWIDTH/3)):
        buttons[x,y] = Buttons(x, y)
            

class CellBlock:
    def __init__(self, x , y, CELLSIZE):
        self.highlighted = 0
        self.x = x*CELLSIZE
        self.y = y*CELLSIZE
        self.rect = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
        self.life = 0

    def drawCell(self, screen):
        options = {0:'white', 1:'gray68', 2:'gray79'}
        pygame.draw.rect(screen, pygame.Color(options.get(self.highlighted, 'white')), self.rect)

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted

    def setLife(self, life):
        self.life = life

class Buttons:
    def __init__(self, x, y):
        self.name = "button"
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, int(WINDOWHEIGHT*0.70), BUTTONWIDTH, BUTTONHEIGHT)
   
    def drawbutton(self, screen):
        pygame.draw.rect(screen, pygame.Color('gray'), self.rect)

def drawCells():
    for x in range(numOfCells):
        for y in range(numOfCells):
            cells[x,y].drawCell(screen)

def drawButtons():
    y = 0
    #for x in range(int((GRIDWIDTH/3 - BUTTONWIDTH)/2), GRIDWIDTH, int(GRIDWIDTH/3)):
    buttons[playButtonPos,0].drawbutton(screen)
        #Displaying solve button
    '''if x == 10:
            solveButton = BASICFONT.render(str("Solve"), True, (0,0,0))
            screen.blit(solveButton, (x+10,int(WINDOWHEIGHT*0.73) ))'''


def clicked(pos):
    if pos[1]>0 and pos[1]<GRIDHEIGHT:
        #print(pos)
        for x in range(numOfCells):
            for y in range(numOfCells):
                #cells[x,y].setHighlighted(random.randint(0,2))
                if cells[x,y].rect.collidepoint(pos):
                    if cells[x,y].highlighted == 1:
                        cells[x,y].setHighlighted(0)
                        cells[x,y].setLife(0)
                    elif cells[x,y].highlighted == 0:
                        cells[x,y].setHighlighted(1)
                        cells[x,y].setLife(1)
    if buttons[playButtonPos,0].rect.collidepoint(pos):
        playGame()
        lifeAlert()
        

def playGame():
    newCells = cells
    for x in range(numOfCells):
            for y in range(numOfCells):
                if cells[x,y].highlighted:
                    if checkNeighbours(x,y) == 2:
                        newCells[x,y].setLife(1)
                    if checkNeighbours(x,y) == 3:
                        newCells[x,y].setLife(1)
                    if checkNeighbours(x,y) < 2:
                        newCells[x,y].setLife(0)
                    if checkNeighbours(x,y) >= 4:
                        newCells[x,y].setLife(0)
                if cells[x,y].highlighted == 0:
                    if checkNeighbours(x,y) == 3:
                        newCells[x,y].setLife(1)
                print(checkNeighbours(1,1))
                    
    
    
    

    #Any cell with 2/3 neighbours survive
    #Any cell with 3<neighbours dies
    #Any dead cell with exactly 3 live neighbours becomes alive

def checkNeighbours(x,y):
    neighbours = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if (i,j) != (x,y):
                try:
                    if cells[i,j].highlighted:
                        neighbours += 1
                        if x == 1 and y == 1:
                            pass
                except:
                    pass
                '''if x == 1 and y == 1:
                    print(i,j, neighbours)'''           
    return neighbours
        
def lifeAlert():
    for x in range(numOfCells):
            for y in range(numOfCells):
                if cells[x,y].life:
                    cells[x,y].setHighlighted(1)
                else:
                    cells[x,y].setHighlighted(0)

main()