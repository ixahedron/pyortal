from configuration import *
import pygame

class Portal(pygame.sprite.Sprite):
  
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(portal_blue_image), (portal_width, portal_height))

    self.rect = self.image.get_rect()


class Portal_opened(Portal):
  
  def __init__(self, width, height, is_blue, direction):
    Portal.__init__(self)

    if is_blue:
      image_used = portal_blue_image
    else:
      image_used = portal_orange_image

    self.image = pygame.transform.scale(pygame.image.load(image_used), (width, height))
    
    self.rect = self.image.get_rect()

    self.direction = direction
