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
    
  def set_in_motion(self, dist):
    if dist < 0:
      if self.direction == RIGHT:
        self.direction = LEFT
        self.image = pygame.transform.flip(self.image, True, False)
    else:
      if self.direction == LEFT:
        self.direction = RIGHT
        self.image = pygame.transform.flip(self.image, True, False)

    self.speed_x = dist if self.hands_empty else 0.75 * dist

  def move_x(self):
    MoveableObject.move_x(self)

    if not self.hands_empty:
      if self.direction == LEFT:
        self.holded_object.rect.right = self.rect.left - self.rect.width / 4
      else:
        self.holded_object.rect.left = self.rect.right + self.rect.width / 4
    
  def move_y(self):
    MoveableObject.move_y(self)
    if not self.hands_empty:
      self.holded_object.rect.y = self.rect.y

  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
    cube_collisions = pygame.sprite.spritecollide(self, self.level.cubes, False)
    self.rect.y -= 2

    if len(platform_collisions + cube_collisions) > 0 or self.rect.bottom >= screen_y:
      if self.hands_empty:
        self.speed_y = speed
      else:
        self.speed_y = 0.7 * speed

  def on_goal(self):
    return pygame.sprite.spritecollideany(self, self.level.exit) is not None

  def horizontal_collision_handler(self, block_collisions, with_moveable = False):
    if with_moveable:
      for block in block_collisions:
        if self.hands_empty or block.order_number is not self.holded_object.order_number:
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
    delta = self.rect.width / 4
    if self.direction == LEFT:
      self.rect.x -= delta
    self.rect.width += delta
    cubes_nearby = sorted(pygame.sprite.spritecollide(self, self.level.cubes, False), key = lambda c: (abs(c.rect.x - self.rect.x), -c.rect.y))
    self.rect.width -= delta
    if self.direction == LEFT:
      self.rect.x += delta

    if len(cubes_nearby) > 0:
      self.hands_empty = False
      self.holded_object = cubes_nearby[0]
      self.holded_object.holded = True


  def drop_holded(self):
    self.holded_object.holded = False
    self.holded_object.movement_key_pressed = False
    self.hands_empty = True
  
