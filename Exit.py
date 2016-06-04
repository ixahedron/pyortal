from configuration import *
from geometry import calculateIntersectPoint
import pygame

class Exit(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(exit_image), (exit_width, exit_height))

    self.rect = self.image.get_rect()

    self.portalable = False
