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
drawing = False
erasure = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")
screen.fill(pygame.Color("lightblue"))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    switchDrawing()
                if event.key == pygame.K_w:
                    switchErasure()
        pos = pygame.mouse.get_pos()
        if drawing == True:
            draw(pos)
        if erasure == True:
            erase(pos)
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
numOfCells = 20
CELLSIZE = int(width/numOfCells)
BUTTONHEIGHT = GRIDWIDTH*(50/270)
BUTTONWIDTH = GRIDWIDTH*(70/270)
buttonSpace = int(GRIDWIDTH/3)
playButtonPos = int((GRIDWIDTH/3 - BUTTONWIDTH)/2)
drawButtonPos = playButtonPos + buttonSpace

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
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, int(WINDOWHEIGHT*0.70), BUTTONWIDTH, BUTTONHEIGHT)
   
    def drawPlayButton(self, screen):
        pygame.draw.rect(screen, pygame.Color('gray'), self.rect)
    
    def drawDrawButton(self, screen):
        pygame.draw.rect(screen, pygame.Color('black'), self.rect)
    
    def drawInputBox(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect)



def drawCells():
    for x in range(numOfCells):
        for y in range(numOfCells):
            cells[x,y].drawCell(screen)

def drawButtons():
    y = 0
    #for x in range(int((GRIDWIDTH/3 - BUTTONWIDTH)/2), GRIDWIDTH, int(GRIDWIDTH/3)):
    buttons[playButtonPos,0].drawPlayButton(screen)
    buttons[drawButtonPos, 0].drawDrawButton(screen)
        #Displaying solve button
    '''if x == 10:
            solveButton = BASICFONT.render(str("Solve"), True, (0,0,0))
            screen.blit(solveButton, (x+10,int(WINDOWHEIGHT*0.73) ))'''


def clicked(pos, selected=True):
    global drawing
    if pos[1]>0 and pos[1]<GRIDHEIGHT:
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
        '''continue = true
        while no new events, and while continue = true
            for all cells check if they are alive
                if they are alive:
                    continue = true
                    time.sleep(0.5 seconds)
                    playGame()
                if they aren't alive:
                    continue =false'''
        playGame()
        lifeAlert()
    if buttons[drawButtonPos,0].rect.collidepoint(pos):
        time.sleep(2)
        switchDrawing()
        

def draw(pos):
    for x in range(numOfCells):
            for y in range(numOfCells):
                if cells[x,y].rect.collidepoint(pos):
                    if cells[x,y].highlighted == 0:
                            cells[x,y].setHighlighted(1)
                            cells[x,y].setLife(1)
def erase(pos):
    for x in range(numOfCells):
            for y in range(numOfCells):
                if cells[x,y].rect.collidepoint(pos):
                    if cells[x,y].highlighted == 1:
                            cells[x,y].setHighlighted(0)
                            cells[x,y].setLife(0)


#make action a class??
def switchDrawing():
    global drawing
    if drawing == True:
            drawing = False
    elif drawing == False:
            drawing = True

def switchErasure():
    global erasure
    if erasure == True:
        erasure = False
    elif erasure == False:
        erasure = True
    

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
    return neighbours
        
def lifeAlert():
    for x in range(numOfCells):
            for y in range(numOfCells):
                if cells[x,y].life:
                    cells[x,y].setHighlighted(1)
                else:
                    cells[x,y].setHighlighted(0)



main()