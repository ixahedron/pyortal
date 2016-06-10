import pygame
from configuration import *
from MoveableObject import *

class Player(MoveableObject):
  def __init__(self):
    MoveableObject.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
    self.rect = self.image.get_rect()

    self.portalable = True
    
  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    self.rect.y -= 2

    if len(platform_collisions) > 0 or self.rect.bottom >= screen_y:
      self.speed_y = speed

  def on_goal(self):
    return pygame.sprite.spritecollideany(self, self.level.exit) is not None

