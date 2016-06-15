from configuration import *
import pygame

class Button(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()

    self.portal_supporting = False
    self.pressed = False

    self.door = None

  def press(self):
    self.pressed = True
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h / 2))
    self.rect = self.image.get_rect()

    self.door.open()
    
  def unpress(self):
    self.pressed = False
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()

    self.door.close()
