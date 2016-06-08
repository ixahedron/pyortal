import pygame
from configuration import *

class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(player_image), (player_width, player_height))
    
    self.rect = self.image.get_rect()

    self.movement_key_pressed = False
    
    self.speed_x = 0
    self.speed_y = 0

    self.direction = RIGHT
    
    self.level = None

  def update(self):
    # Change the vertical velocity according to gravity shift
    self.determine_gravity_shift()

    # Horizontal movement
    self.rect.x += self.speed_x
    if not self.movement_key_pressed:
      if self.speed_x > friction:
        self.speed_x -= friction
      elif self.speed_x < -friction:
        self.speed_x += friction
      else:  
        self.speed_x = 0

    # Portal check
    if pygame.sprite.spritecollide(self, self.level.portal_blue, False):
      if self.level.portal_orange.sprite is not None:
        self.rect.x = self.level.portal_orange.sprite.rect.x + self.level.portal_orange.sprite.direction[0]
        self.rect.y = self.level.portal_orange.sprite.rect.y + self.level.portal_orange.sprite.direction[1]
        self.change_direction(True)
    elif pygame.sprite.spritecollide(self, self.level.portal_orange, False):
      if self.level.portal_blue.sprite is not None:
        self.rect.x = self.level.portal_blue.sprite.rect.x + self.level.portal_blue.sprite.direction[0]
        self.rect.y = self.level.portal_blue.sprite.rect.y + self.level.portal_blue.sprite.direction[1]
        self.change_direction(False)

    # Collisions after horizontal movement
    block_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    for block in block_collisions:
      if self.speed_x > 0:
        self.rect.right = block.rect.left
      elif self.speed_x < 0:
        self.rect.left = block.rect.right

    # Vertical movement
    self.rect.y += self.speed_y

    # Portal check
    if pygame.sprite.spritecollide(self, self.level.portal_blue, False):
      if self.level.portal_orange.sprite is not None:
        self.rect.x = self.level.portal_orange.sprite.rect.x + self.level.portal_orange.sprite.direction[0]
        self.rect.y = self.level.portal_orange.sprite.rect.y + self.level.portal_orange.sprite.direction[1]
        self.change_direction(True)
    elif pygame.sprite.spritecollide(self, self.level.portal_orange, False):
      if self.level.portal_blue.sprite is not None:
        self.rect.x = self.level.portal_blue.sprite.rect.x + self.level.portal_blue.sprite.direction[0]
        self.rect.y = self.level.portal_blue.sprite.rect.y + self.level.portal_blue.sprite.direction[1]
        self.change_direction(False)

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
    if dist < 0:
      if self.direction == RIGHT:
        self.direction = LEFT
        self.image = pygame.transform.flip(self.image, True, False)
    else:
      if self.direction == LEFT:
        self.direction = RIGHT
        self.image = pygame.transform.flip(self.image, True, False)

    self.speed_x = dist

  def stop(self):
    self.speed_x = 0

  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    self.rect.y -= 2

    if len(platform_collisions) > 0 or self.rect.bottom >= screen_y:
      self.speed_y = speed

  def on_goal(self):
    return pygame.sprite.spritecollideany(self, self.level.exit) is not None

  def determine_gravity_shift(self):
    if self.speed_y < maximum_vertical_velocity:
      self.speed_y = 1 if self.speed_y == 0 else self.speed_y + gravity

    if self.rect.y >= screen_y - self.rect.height and self.speed_y >= 0:
      self.speed_y = 0
      self.rect.y = screen_y - self.rect.height

  def change_direction(self, out_of_the_blue):
    fst_portal_dir = self.level.portal_blue.sprite.direction
    snd_portal_dir = self.level.portal_blue.sprite.direction
    if out_of_the_blue:
      snd_portal_dir = self.level.portal_orange.sprite.direction
    else:
      fst_portal_dir = self.level.portal_orange.sprite.direction
    
    # This is just horrible. TODO: do some school-level geometry magic and figure out how to generalise this calculation.
    if fst_portal_dir == LEFT:
      if snd_portal_dir == LEFT:
        self.movement_key_pressed = False
        self.speed_x *= -1
      if snd_portal_dir == DOWN:
        self.speed_y = abs(self.speed_x)
        self.speed_x = 0
      if snd_portal_dir == UP:
        self.speed_y = -abs(self.speed_x)
        self.speed_x = 0
    if fst_portal_dir == RIGHT:
      if snd_portal_dir == RIGHT:
        self.movement_key_pressed = False
        self.speed_x *= -1
      if snd_portal_dir == DOWN:
        self.speed_y = abs(self.speed_x)
        self.speed_x = 0
      if snd_portal_dir == UP:
        self.speed_y = -abs(self.speed_x)
        self.speed_x = 0
    if fst_portal_dir == UP:
      if snd_portal_dir == UP:
        self.speed_y *= -1
      if snd_portal_dir == RIGHT:
        self.speed_x = abs(self.speed_y)
        self.speed_y = 1
      if snd_portal_dir == LEFT:
        self.speed_x = -abs(self.speed_y)
        self.speed_y = 1
    if fst_portal_dir == DOWN:
      if snd_portal_dir == DOWN:
        self.speed_y *= -1
      if snd_portal_dir == RIGHT:
        self.speed_x = abs(self.speed_y)
        self.speed_y = 1
      if snd_portal_dir == LEFT:
        self.speed_x = -abs(self.speed_y)
        self.speed_y = 1
