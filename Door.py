from configuration import *
from geometry import calculateIntersectPoint
import pygame
import pygame.time


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

    door_opened =  "res/electric_door_opening_1.wav"
    door_snd = pygame.mixer.Sound(door_opened)
    door_snd.play()
    x = self.rect.x
    b = self.rect.bottom
    # self.image = pygame.transform.scale(pygame.image.load(door_image), (door_w, door_h / 10))
    self.image = pygame.transform.scale(self.image, (door_w, int(0.1 * door_h)))
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
  
  def intersection(self, p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2

    from_left = False
    from_top = False

    if x1 < x2:
      from_left = True
    if y1 < y2:
      from_top = True

    cip = lambda p3, p4: calculateIntersectPoint(p1, p2, p3, p4)

    if from_left:
      intersection_point = cip(self.rect.topleft, self.rect.bottomleft) 
    else:
      intersection_point = cip(self.rect.topright, self.rect.bottomright) 
      
    if intersection_point is None:
      if from_top:
        intersection_point = cip(self.rect.topleft, self.rect.topright) 
      else:
        intersection_point = cip(self.rect.bottomleft, self.rect.bottomright) 

    return intersection_point is not None
