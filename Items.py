from configuration import *
from MoveableObject import *
import pygame

class Cube(MoveableObject):

  def __init__(self, order_number):
    MoveableObject.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(cube_image), (cube_edge, cube_edge))
    self.rect = self.image.get_rect()

    self.portalable = True

    self.holdable = True
    self.holded = False

    self.order_number = order_number
  
  def set_in_motion(self, dist):
    if dist < 0:
      if self.direction == RIGHT:
        self.direction = LEFT
        self.image = pygame.transform.flip(self.image, True, False)
    else:
      if self.direction == LEFT:
        self.direction = RIGHT
        self.image = pygame.transform.flip(self.image, True, False)

    if not self.holded:
      self.speed_x = dist

  def collided_callback(self, left, right):
    return left.order_number is not right.order_number and MoveableObject.collided_callback(self, left, right)
  
  def determine_gravity_shift(self):
    if self.holded:
      self.speed_y = 0
    else:
      MoveableObject.determine_gravity_shift(self)

