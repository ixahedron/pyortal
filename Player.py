import pygame
from pygame.locals import *
from configuration import *

class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
    
    self.rect = self.image.get_rect()
    
    self.speed_x = 0
    self.speed_y = 0
    
    self.level = None

  def update(self):
    # Change the vertical velocity according to gravity shift
    self.determine_gravity_shift()

    # Horizontal movement
    self.rect.x += self.speed_x

    # Collisions after vertical movement
    block_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    for block in block_collisions:
      if self.speed_x > 0:
        self.rect.right = block.rect.left
      elif self.speed_x < 0:
        self.rect.left = block.rect.right

    # Vertical movement
    self.rect.y += self.speed_y

    # Collisions after vertical movement
    block_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    for block in block_collisions:
      if self.speed_y > 0:
        self.rect.bottom = block.rect.top
      elif self.speed_y < 0:
        self.rect.top = block.rect.bottom

      # If the player is now standing on a platform, set the vertical velocity to zero
      self.speed_y = 0

  def move_x(self, dist):
    self.speed_x = dist

  def stop(self):
    self.speed_x = 0

  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    self.rect.y -= 2

    if len(platform_collisions) > 0 or self.rect.bottom >= screen_y:
      self.speed_y = speed

  def determine_gravity_shift(self):
    self.speed_y = 1 if self.speed_y == 0 else self.speed_y + 0.35

    if self.rect.y >= screen_y - self.rect.height and self.speed_y >= 0:
      self.speed_y = 0
      self.rect.y = screen_y - self.rect.height
