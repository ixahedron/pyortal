import pygame

class DynamicRect():

    width = 0
    height = 0

    posX = 0
    posY = 0

    color = (255,255,255)
    surface = None    

    def draw(self):
        pygame.draw.rect(self.surface, self.color, [self.posX, self.posY, self.width, self.height],0)

    def setSize(self, newWidth, newHeight):
        self.width = newWidth
        self.height = newHeight        

    def setPosition(self, newPosX, newPosY):
        self.posX = newPosX
        self.posY = newPosY

    

class PlatformRect(DynamicRect):

    def __init__(self, levelData, initSurface):
        self.setSize(levelData[0], levelData[1])
        self.setPosition(levelData[2], levelData[3])
        self.surface = initSurface
        if levelData[4] == True:
            self.color = (75,75,75)
        else:
            self.color = (230, 230, 230)
        
        
class CubeRect(DynamicRect):

    def __init__(self, cubeData, initSurface):

        cubeSize = 10
        
        self.setSize(cubeSize, cubeSize)
        self.setPosition(cubeData[0], cubeData[1])
        self.surface = initSurface
        self.color = (0,255,0)

class ButtonRect(DynamicRect):

    def __init__(self, buttonData, initSurface):

        buttonSize = 10
        
        self.setSize(buttonSize*2, buttonSize)
        self.setPosition(buttonData[0], buttonData[1])
        self.surface = initSurface
        self.color = (200,0,0)

    def setPosition(self, newPosX, newPosY):
        self.posX = newPosX
        self.posY = newPosY - 15


class DoorRect(DynamicRect):

    def __init__(self, doorData, initSurface):

        doorSize = 10
        
        self.setSize(doorSize, doorSize*16)
        self.setPosition(doorData[0], doorData[1])
        self.surface = initSurface
        self.color = (0,0,255)

    def setPosition(self, newPosX, newPosY):
        self.posX = newPosX
        self.posY = newPosY - 160
        
