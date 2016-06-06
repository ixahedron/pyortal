from configuration import *
from geometry import calculateIntersectPoint
import pygame

class Platform(pygame.sprite.Sprite):

  def __init__(self, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(platform_image), (width, height))

    self.rect = self.image.get_rect()

    self.portalable = True

  def intersection(self, p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2

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

    cip = lambda p3, p4: calculateIntersectPoint(p1, p2, p3, p4)

    if from_left:
      intersection_point = cip(top_left, bottom_left) 
    else:
      intersection_point = cip(top_right, bottom_right) 
      
    if intersection_point is None:
      if from_top:
        intersection_point = cip(top_left, top_right) 
      else:
        intersection_point = cip(bottom_left, bottom_right) 

    self.intersection_point = intersection_point
    return intersection_point

  def get_portal_direction(self):
    ip = self.intersection_point
    x = self.rect.x
    y = self.rect.y
    w = self.rect.width
    h = self.rect.height

    if x < ip[0] < x+w:
      if ip[1] == y:
        return UP
      elif ip[1] == y+h:
        return DOWN
    elif y <= ip[1] <= y+h:
      if ip[0] == x:
        return LEFT
      elif ip[0] == x+w:
        return RIGHT
    return None