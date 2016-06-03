from configuration import *
import pygame

class Platform(pygame.sprite.Sprite):

  def __init__(self, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(platform_image), (width, height))

    self.rect = self.image.get_rect()

    self.portalable = True

  def intersection(x1, y1, x2, y2):
    from_left = False
    from_top = False

    top_left = (self.rect.x, self.rect.y)
    bottom_left = (self.rect.x, self.rect.y + self.rect.height)
    top_right = (self.rect.x + self.rect.width, self.rect.y)
    bottom_right = (self.rect.x + self.rect.width, self.rect.y + self.rect.height)

    if x1 < x2:
      from_left = True
    if y1 < y2:
      from_top = True

    if from_left:
      
      intersection_point = None # TODO calculation
      
      if intersection_point is None:
        if from_top:
          intersection_point = None # TODO calculation
        else:
          intersection_point = None # TODO calculation
  
    else:
      intersection_point = None # TODO calculation
      
      if intersection_point is None:
        if from_top:
          intersection_point = None # TODO calculation
        else:
          intersection_point = None # TODO calculation
    
    return intersection_point
