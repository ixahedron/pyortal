import os, pygame
from pygame.locals import *
from DynamicRect import *


### Variables ###

# Position where the Window opens
WindowPosX = 0
WindowPosY = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WindowPosX, WindowPosY)

pygame.init()

# InfoObject to get the width and height of the monitor
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w - 380, infoObject.current_h - 280), HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Map Editor')


darkgrey = (75,75,75)
lightgrey = (230, 230, 230)
block_size = 50

# New Surface for the Background
background = pygame.Surface(screen.get_size()) 
background.fill(lightgrey)      
background = background.convert()  # Convert Surface to make blitting faster

objects = pygame.Surface(screen.get_size())



level = []
cubes = []
buttons = []
doors = []



### Methods ###

        
def endGame():
    pygame.display.quit()
    pygame.quit()
    quit()

def openLevelFile(filename):
    with open(filename, 'r') as levelfile:               #Context Manager for automatic close() and Exception-Handling
        ## save()
        
        levelfileAsString = "global level\n" + "global cubes\n" + "global buttons\n" + "global doors\n" + levelfile.read()        
        exec(levelfileAsString)
        drawLevel()
        
def drawPlatforms():
    for platformData in level:
        platform = PlatformRect(platformData, objects)        
        platform.draw()

    
def drawCubes():
    for cubeData in cubes:
        cube = CubeRect(cubeData, objects)     
        cube.draw()

def drawButtons():
    for buttonData in buttons:
        button = ButtonRect(buttonData, objects)     
        button.draw()

def drawDoors():
    for doorData in doors:
        door = DoorRect(doorData, objects)     
        door.draw() 
        
def drawLevel():
    drawPlatforms()
    drawCubes()
    drawButtons()
    drawDoors()


### EditorLoop ###

while True:
    pygame.event.pump()
    event=pygame.event.wait()       #  for event in pygame.event.get():
    
    background.fill(darkgrey)
    #pygame.draw.rect(objects, lightgrey, [100, 100, 100, 10])
    
    screen.blit(background, (0, 0))
    screen.blit(objects, (0, 0))
    
    
    if event.type==QUIT:
        endGame()
    elif event.type==VIDEORESIZE:
        screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
    
        pygame.display.flip()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            pass
        elif event.key == pygame.K_RIGHT:
            pass
        elif event.key == pygame.K_UP:
            pass
        elif event.key == pygame.K_DOWN:
            openLevelFile('Levels/level1.txt')          
    
    pygame.display.update()





    








