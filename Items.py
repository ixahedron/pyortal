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
    self.holded_by = None

    self.order_number = order_number
  
  def set_in_motion(self, dist):
    if dist < 0 and self.direction is RIGHT:
      self.flip()
      if self.holded:
        self.rect.right = self.holded_by.rect.left - self.holded_by.rect.width / 4
    elif dist > 0 and self.direction is LEFT:
      self.flip()
      if self.holded:
        self.rect.left = self.holded_by.rect.right + self.holded_by.rect.width / 4

    self.speed_x = dist if not self.holded else 0.75 * dist

  def collided_callback(self, left, right):
    return left.order_number is not right.order_number and MoveableObject.collided_callback(self, left, right)
  
  def determine_gravity_shift(self):
    MoveableObject.determine_gravity_shift(self)

    if self.holded and self.holded_by.speed_y == 0 and self.rect.y >= self.holded_by.rect.y and self.speed_y > 0:
      self.speed_y = 0
      self.rect.y = self.holded_by.rect.y

