from configuration import *
import pygame

class Platform(pygame.sprite.Sprite):

  def __init__(self, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(platform_image), (width, height))

    self.rect = self.image.get_rect()

    self.portalable = True
