from configuration import *
import pygame

class Portal(pygame.sprite.Sprite):
  
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(portal_blue_image), (portal_width, portal_height))

    self.rect = self.image.get_rect()


class Portal_blue(Portal):
  
  def __init__(self, width, height):
    Portal.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(portal_blue_image), (width, height))
    
    self.rect = self.image.get_rect()


class Portal_orange(Portal):
  
  def __init__(self, width, height):
    Portal.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(portal_orange_image), (width, height))
    
    self.rect = self.image.get_rect()

