from configuration import *
import pygame

class Door(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    # self.image = pygame.transform.scale(pygame.image.load(door_image), (door_w, door_h))
    self.image = pygame.Surface([door_w, door_h])
    self.image.fill(BLUE)
    self.rect = self.image.get_rect()

    self.portal_supporting = False
    self.closed = True

    self.button = None

  def open(self):
    self.closed = False

    x = self.rect.x
    b = self.rect.bottom
    # self.image = pygame.transform.scale(pygame.image.load(door_image), (door_w, door_h / 10))
    self.image = pygame.transform.scale(self.image, (door_w, door_h / 10))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.bottom = b
    
  def close(self):
    self.closed = True
    
    x = self.rect.x
    b = self.rect.bottom
    # self.image = pygame.transform.scale(pygame.image.load(door_image), (door_w, door_h))
    self.image = pygame.transform.scale(self.image, (door_w, door_h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.bottom = b
