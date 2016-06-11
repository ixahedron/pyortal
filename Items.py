from configuration import *
from MoveableObject import *
import pygame

class Cube(MoveableObject):

  def __init__(self, ordering_number):
    MoveableObject.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(cube_image), (cube_edge, cube_edge))
    self.rect = self.image.get_rect()

    self.portalable = True

    self.ordering_number = ordering_number

  def collided_callback(self, left, right):
    return left.ordering_number is not right.ordering_number and MoveableObject.collided_callback(self, left, right)
