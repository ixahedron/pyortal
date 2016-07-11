import pygame
from configuration import *

class MoveableObject(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.speed_x = 0
    self.speed_y = 0

    self.direction = RIGHT
    
    self.level = None

    self.movement_key_pressed = False

    self.portalable = False

  def update(self):
    # Change the vertical velocity according to gravity shift
    self.determine_gravity_shift()

    # Horizontal movement
    self.move_x()

    # Portal check
    self.through_portal_check()

    # Collisions after horizontal movement
    block_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    block_collisions += pygame.sprite.spritecollide(self, self.level.doors, False)
    cubes_collisions = pygame.sprite.spritecollide(self, self.level.cubes, False, self.collided_callback)
    buttons_collisions = pygame.sprite.spritecollide(self, self.level.buttons, False)
    self.horizontal_collision_handler(block_collisions)
    self.horizontal_collision_handler(cubes_collisions, True)
    self.horizontal_collision_handler(buttons_collisions)

    # Vertical movement
    self.move_y()

    # Portal check
    self.through_portal_check()

    # Collisions after vertical movement
    block_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    block_collisions += pygame.sprite.spritecollide(self, self.level.doors, False)
    cubes_collisions = pygame.sprite.spritecollide(self, self.level.cubes, False, self.collided_callback)
    buttons_collisions = pygame.sprite.spritecollide(self, self.level.buttons, False)
    self.vertical_collision_handler(block_collisions)
    self.vertical_collision_handler(cubes_collisions, True)
    self.vertical_collision_handler(buttons_collisions)

  def set_in_motion(self, dist):
    if (dist < 0 and self.direction is RIGHT) or (dist > 0 and self.direction is LEFT):
      self.flip()
        
    self.speed_x = dist

  def move_x(self):
    self.rect.x += self.speed_x
    if not self.movement_key_pressed:
      if self.speed_x > friction:
        self.speed_x -= friction
      elif self.speed_x < -friction:
        self.speed_x += friction
      else:  
        self.speed_x = 0
    
  def move_y(self):
      self.rect.y += self.speed_y

  def stop(self):
    self.speed_x = 0

  def determine_gravity_shift(self):
    if self.speed_y < maximum_vertical_velocity:
      self.speed_y = 1 if self.speed_y == 0 else self.speed_y + gravity

    if self.rect.y >= screen_y - self.rect.height and self.speed_y >= 0:
      self.speed_y = 0
      self.rect.y = screen_y - self.rect.height

  def collided_callback(self, left, right):
    return pygame.sprite.collide_rect(left, right)

  def through_portal_check(self):
    # Portal check
    if self.portalable:
      fst = None
      snd = None
      if pygame.sprite.spritecollideany(self, self.level.portal_blue):
        fst = self.level.portal_blue.sprite
        snd = self.level.portal_orange.sprite
      elif pygame.sprite.spritecollideany(self, self.level.portal_orange):
        snd = self.level.portal_blue.sprite
        fst = self.level.portal_orange.sprite
      if fst is not None and snd is not None:
        delta = 0
        if fst.direction is DOWN or fst.direction is UP:
          if abs(fst.rect.x - snd.rect.x) > 20:
            delta = self.rect.x - fst.rect.x
        else:
          if abs(fst.rect.y - snd.rect.y) > 20:
            delta = self.rect.y - fst.rect.y
        self.rect.x = snd.rect.x + (0 if snd.direction[1] == 0 else delta) + snd.direction[0]
        self.rect.y = snd.rect.y + (0 if snd.direction[0] == 0 else delta) + snd.direction[1]
        self.change_direction(fst is self.level.portal_blue.sprite)

  def flip(self):
    self.direction = LEFT if self.direction is RIGHT else RIGHT
    self.image = pygame.transform.flip(self.image, True, False)

  def change_direction(self, out_of_the_blue):
    fst_portal_dir = self.level.portal_blue.sprite.direction
    snd_portal_dir = self.level.portal_blue.sprite.direction
    if out_of_the_blue:
      snd_portal_dir = self.level.portal_orange.sprite.direction
    else:
      fst_portal_dir = self.level.portal_orange.sprite.direction
    
    # This is just horrible. TODO: do some school-level geometry magic and figure out how to generalise this calculation.
    if fst_portal_dir is LEFT:
      if snd_portal_dir is LEFT:
        self.movement_key_pressed = False
        self.speed_x *= -1
      if snd_portal_dir is DOWN:
        self.speed_y = abs(self.speed_x)
        self.speed_x = 0
      if snd_portal_dir is UP:
        self.speed_y = -abs(self.speed_x)
        self.speed_x = 0
    if fst_portal_dir is RIGHT:
      if snd_portal_dir is RIGHT:
        self.movement_key_pressed = False
        self.speed_x *= -1
      if snd_portal_dir is DOWN:
        self.speed_y = abs(self.speed_x)
        self.speed_x = 0
      if snd_portal_dir is UP:
        self.speed_y = -abs(self.speed_x)
        self.speed_x = 0
    if fst_portal_dir is UP:
      if snd_portal_dir is UP:
        self.speed_y *= -1
      if snd_portal_dir is RIGHT:
        self.movement_key_pressed = False
        self.speed_x = abs(self.speed_y)
        self.speed_y = 1
      if snd_portal_dir is LEFT:
        self.movement_key_pressed = False
        self.speed_x = -abs(self.speed_y)
        self.speed_y = 1
    if fst_portal_dir is DOWN:
      if snd_portal_dir is DOWN:
        self.speed_y *= -1
      if snd_portal_dir is RIGHT:
        self.movement_key_pressed = False
        self.speed_x = abs(self.speed_y)
        self.speed_y = 1
      if snd_portal_dir is LEFT:
        self.movement_key_pressed = False
        self.speed_x = -abs(self.speed_y)
        self.speed_y = 1

  def horizontal_collision_handler(self, block_collisions, with_moveable = False):
    for block in block_collisions:
      if self.speed_x > 0:
        self.rect.right = block.rect.left
      elif self.speed_x < 0:
        self.rect.left = block.rect.right
   
  def vertical_collision_handler(self, block_collisions, with_moveable = False):
    for block in block_collisions:
      if self.speed_y > 0:
        self.rect.bottom = block.rect.top
      elif self.speed_y < 0:
        self.rect.top = block.rect.bottom

      # If the item is now on a platform, set the vertical velocity to zero
      self.speed_y = 0
