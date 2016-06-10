from configuration import *
from MoveableObject import *
import pygame

class Cube(MoveableObject):

  def __init__(self):
    MoveableObject.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(cube_image), (cube_edge, cube_edge))
    self.rect = self.image.get_rect()

    self.portalable = True
