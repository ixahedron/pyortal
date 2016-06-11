import pygame
from configuration import *
from MoveableObject import *

class Player(MoveableObject):
  def __init__(self):
    MoveableObject.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
    self.rect = self.image.get_rect()

    self.portalable = True

    self.hands_empty = True
    self.holded_object = pygame.sprite.GroupSingle()
    
  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    self.rect.y -= 2

    if len(platform_collisions) > 0 or self.rect.bottom >= screen_y:
      if self.hands_empty:
        self.speed_y = speed
      else:
        self.speed_y = 0.7 * speed

  def on_goal(self):
    return pygame.sprite.spritecollideany(self, self.level.exit) is not None

  def horizontal_collision_handler(self, block_collisions, with_moveable = False):
    if with_moveable:
      for block in block_collisions:
        if self.speed_x > 0:
          self.rect.right = block.rect.left
        elif self.speed_x < 0:
          self.rect.left = block.rect.right
        block.speed_x = 0.4 * self.speed_x
    else:
      for block in block_collisions:
        if self.speed_x > 0:
          self.rect.right = block.rect.left
        elif self.speed_x < 0:
          self.rect.left = block.rect.right


  def try_pickup(self):
    # cubes_nearby = pygame.sprite.spritecollide(self, self.level.cubes, False)
    pass

  def drop_holded(self):
    self.holded_object.holded = False
    self.hands_empty = True
