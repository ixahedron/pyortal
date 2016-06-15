from configuration import *
from geometry import calculateIntersectPoint
import pygame

class Button(pygame.sprite.Sprite):

  def __init__(self, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()

    self.portal_supporting = False
    self.pressed = False

  def press(self):
    self.pressed = True
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h / 2))
    self.rect = self.image.get_rect()
    
  def unpress(self):
    self.pressed = False
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()
