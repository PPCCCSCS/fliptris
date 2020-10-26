import os, sys
from random import randint, choice
import pygame
from pygame.locals import *

if not pygame.font: print("Warning: fonts disabled")
if not pygame.mixer: print("Warning: sound disabled")

print("Initializing Pygame Next")

pygame.init()

"""
NAUGHTY GLOBAL VARIABLE SECTION
"""

WHITE     = 255,255,255
BLACK     = 0,0,0
CYAN      = 0,255,255
YELLOW    = 255,255,0
PURPLE    = 128,0,128
GREEN     = 0,128,0
RED       = 255,0,0
BLUE      = 0,0,255
ORANGE    = 255,165,0

# Tetrominos have single-letter names
MINOS     = ('I','O','T','S','Z','J','L')

# Cardinal Directions
NESW      = ('N','E','S','W')

minosSet = set()
 
I = pygame.image.load("images\\lightblue.png")
O = pygame.image.load("images\\yellow.png")
T = pygame.image.load("images\\purple.png")
S = pygame.image.load("images\\green.png")
Z = pygame.image.load("images\\red.png")
J = pygame.image.load("images\\blue.png")
L = pygame.image.load("images\\orange.png")

# playing field position and tile size
BX  = BOARDX    = 40
BY  = BOARDY    = 40
TS  = TILESIZE  = 40

# playing field area
COLUMNS         = 20
ROWS            = 20

# calculate window size
# playing field + info display area
WIDTH     = (BOARDX * 9) + (TILESIZE * COLUMNS)
HEIGHT    = (BOARDY * 2) + (TILESIZE * ROWS)

# Fliptris Title Top Left Position
FTTL       = [TILESIZE*(COLUMNS+2),BOARDY]
# Next Title Top Left Position
NTTL       = [int(TILESIZE*(COLUMNS+3.5)),BOARDY*4]
# Next Box Top Left Position
NBTL       = [TILESIZE*(COLUMNS+2),TILESIZE*6]
# Playfield Top Left Position
PFTL       = [BOARDX,BOARDY]

# create a clock for flow control
clock = pygame.time.Clock()

# set up font rendering (for title)
pygame.init()
pygame.font.init()
f1 = pygame.font.Font("BAUHS93.TTF",64)
f2 = pygame.font.Font("BAUHS93.TTF",48)
TITLE       = "FLIPTRIS"
textTITLE   = "FLIPTRIS"#"ꙄIЯTꟼI⅃ꟻ"
dispTITLE   = f1.render(textTITLE, True, PURPLE)
rectTITLE = dispTITLE.get_rect()
rectTITLE.topleft=FTTL
# set up font rendering for scoreboard
textNEXT    = "NEXT"
dispNEXT    = f2.render(textNEXT, True, (255,255,0))
rectNEXT    = dispNEXT.get_rect()
rectNEXT.topleft=NTTL

# set up the display area
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))

# BASE CLASS FOR TETROMINOES
class Tetromino:
    def __init__(self,pos,angle='N'):
        self.pos = pos
        self.angle = angle
        self.velocityX = 0.0
        self.velocityY = 0.0
    def rotate(self,hand):
        if hand == 'R':
            self.angle = NESW[(NESW.index(self.angle)+1)%len(NESW)]
        elif hand == 'L':
            self.angle = NESW[(NESW.index(self.angle)-1)%len(NESW)]
    def draw(self):
        if self.angle == 'N':
            self.drawBlocks(self.NORTH)
        elif self.angle == 'W':
            self.drawBlocks(self.WEST)
        elif self.angle == 'S':
            self.drawBlocks(self.SOUTH)
        elif self.angle == 'E':
            self.drawBlocks(self.EAST)
    def drawBlocks(self,matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        for row in range(rows):
            for col in range(cols):
                if matrix[row][col] == 1:
                    screen.blit(self.block,(self.pos[0]+TS*col,self.pos[1]+TS*row))
            
class IMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        self.block = I
        self.pos = pos
        self.angle = angle
        self.NORTH = [[0,0,0,0],
                      [1,1,1,1],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,0,1,0],
                      [0,0,1,0],
                      [0,0,1,0],
                      [0,0,1,0]]
        self.SOUTH = [[0,0,0,0],
                      [0,0,0,0],
                      [1,1,1,1],
                      [0,0,0,0]]
        self.WEST  = [[0,1,0,0],
                      [0,1,0,0],
                      [0,1,0,0],
                      [0,1,0,0]]

class OMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        Tetromino.__init__(self,pos,angle)
        self.block = O
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.WEST  = [[0,1,1,0],
                      [0,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]

class TMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        Tetromino.__init__(self,pos,angle)
        self.block = T
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[0,1,0,0],
                      [1,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,1,0,0],
                      [0,1,1,0],
                      [0,1,0,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,0,0,0],
                      [1,1,1,0],
                      [0,1,0,0],
                      [0,0,0,0]]
        self.WEST  = [[0,1,0,0],
                      [1,1,0,0],
                      [0,1,0,0],
                      [0,0,0,0]]

class SMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        Tetromino.__init__(self,pos,angle)
        self.block = S
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[0,1,1,0],
                      [1,1,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,1,0,0],
                      [0,1,1,0],
                      [0,0,1,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,0,0,0],
                      [0,1,1,0],
                      [1,1,0,0],
                      [0,0,0,0]]
        self.WEST  = [[1,0,0,0],
                      [1,1,0,0],
                      [0,1,0,0],
                      [0,0,0,0]]
            
class ZMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        Tetromino.__init__(self,pos,angle)
        self.block = Z
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[1,1,0,0],
                      [0,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,0,1,0],
                      [0,1,1,0],
                      [0,1,0,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,0,0,0],
                      [1,1,0,0],
                      [0,1,1,0],
                      [0,0,0,0]]
        self.WEST  = [[0,1,0,0],
                      [1,1,0,0],
                      [1,0,0,0],
                      [0,0,0,0]]

class JMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        self.block = J
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[1,0,0,0],
                      [1,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,1,1,0],
                      [0,1,0,0],
                      [0,1,0,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,0,0,0],
                      [1,1,1,0],
                      [0,0,1,0],
                      [0,0,0,0]]
        self.WEST  = [[0,1,0,0],
                      [0,1,0,0],
                      [1,1,0,0],
                      [0,0,0,0]]

class LMino(Tetromino):
    def __init__(self,pos,angle='N'):
        Tetromino.__init__(self,pos,angle)
        Tetromino.__init__(self,pos,angle)
        self.block = L
        self.pos = pos
        self.angle = angle 
        self.NORTH = [[0,0,1,0],
                      [1,1,1,0],
                      [0,0,0,0],
                      [0,0,0,0]]
        self.EAST  = [[0,1,0,0],
                      [0,1,0,0],
                      [0,1,1,0],
                      [0,0,0,0]]
        self.SOUTH = [[0,0,0,0],
                      [1,1,1,0],
                      [1,0,0,0],
                      [0,0,0,0]]
        self.WEST  = [[1,1,0,0],
                      [0,1,0,0],
                      [0,1,0,0],
                      [0,0,0,0]]

def nextBlock():
    nxt = choice(MINOS)
    #print(nxt,end=" ")
    return nxt
    
def draw():
    screen.blit(background, (0,0))
    screen.blit(dispTITLE, rectTITLE)
    screen.blit(dispNEXT, rectNEXT),
    nextMino = nextBlock()
    newMino(nextMino)
    for x in minosSet:
        x.draw()
        x.rotate('L')

    # update everything
    pygame.display.flip()
    clock.tick(1)

def newMino(shape):

    if shape == 'I':
        block = I
    elif shape == 'O':
        block = O
    elif shape == 'T':
        block = T
    elif shape == 'S':
        block = S
    elif shape == 'Z':
        block = Z
    elif shape == 'J':
        block = J
    elif shape == 'L':
        block = L
    drawMino(shape, block, [NBTL[0]+TS,NBTL[1]+TS])

def drawMino(shape, block, pos, angle='N'):
    if shape == 'I':
        IMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'O':
        OMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'T':
        TMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'S':
        SMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'Z':
        ZMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'J':
        JMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    elif shape == 'L':
        LMino([NBTL[0]+TS,NBTL[1]+TS],'N').draw()
    

def main():

    # draw playfield border
    pygame.draw.rect(background, (255,255,0), (BX, BY, (TS * COLUMNS), (TS * ROWS)), 2) 
    pygame.draw.rect(background, (255,255,0), (TS*(COLUMNS+2),TS*6 ,TS*6,TS*4),2)

    minosSet.add( SMino((TS*2 ,TS*2),'N') )
    minosSet.add( OMino((TS*6 ,TS*2),'N') )
    minosSet.add( TMino((TS*10,TS*2),'N') )
    minosSet.add( IMino((TS*14,TS*2),'N') )
    minosSet.add( ZMino((TS*2 ,TS*6),'N') )
    minosSet.add( JMino((TS*6 ,TS*6),'N') )
    minosSet.add( LMino((TS*10,TS*6),'N') )

    while(1):
        
        draw()
        
        
if __name__ == "__main__":
    main()

"""
NOTES:

The basic tetrominoes
Each tetromino has a letter name and several alternative names.

https://tetris.wiki/Tetromino

I -- Light blue; shaped like a capital I; four Minos in a straight line. Other names include straight, stick, and long. This is the only tetromino that can clear four lines outside of cascade games.
O -- Yellow; a square shape; four Minos in a 2×2 square. Other names include square and block.
T -- Purple; shaped like a capital T; a row of three Minos with one added above the center.
S -- Green; shaped like a capital S; two stacked horizontal diminos with the top one offset to the right. Other names include inverse skew and right snake.
Z -- Red; shaped like a capital Z; two stacked horizontal diminos with the top one offset to the left. Other names include skew and left snake.
J -- Blue; shaped like a capital J; a row of three Minos with one added above the left side. Other names include gamma, inverse L, or left gun.
L -- Orange; shaped like a capital L; a row of three Minos with one added above the right side. Other names include right gun.
"""