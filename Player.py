import pygame
from configuration import *
from MoveableObject import *

class Player(MoveableObject):
  def __init__(self, order = 1):

    self.idle_frames = idle_frames_1 if order == 1 else idle_frames_2
    self.run_frames = run_frames_1 if order == 1 else run_frames_2
    self.jump_frames = jump_frames_1 if order == 1 else jump_frames_2
    
    MoveableObject.__init__(self)

    #initialize empty lists
    self.images_idle_r = []
    self.images_idle_l = []
    self.images_run_r = []
    self.images_run_l = []
    self.images_jump_r = []
    self.images_jump_l = []
    
    #load the run frames into a list
    for image in self.idle_frames:
      frame = pygame.transform.scale(pygame.image.load(image), (player_width - 10, player_height))
      self.images_idle_r.append(frame)
    
    for image in self.idle_frames:
      frame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(image), (player_width - 10, player_height) ), True, False)
      self.images_idle_l.append(frame)

    for image in self.run_frames:
      frame = pygame.transform.scale(pygame.image.load(image), (player_width, player_height))
      self.images_run_r.append(frame)

    for image in self.run_frames:
      frame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(image), (player_width, player_height) ), True, False)
      self.images_run_l.append(frame)

    for image in self.jump_frames:
      frame = pygame.transform.scale(pygame.image.load(image), (player_width, player_height))
      self.images_jump_r.append(frame)

    for image in self.jump_frames:
      frame = pygame.transform.flip(pygame.transform.scale(pygame.image.load(image), (player_width, player_height) ), True, False)
      self.images_jump_l.append(frame)

    self.images_list = self.images_idle_r
    self.image = self.images_idle_r[0]
    self.rect = self.image.get_rect()

    self.portalable = True

    self.hands_empty = True
    self.holded_object = pygame.sprite.GroupSingle()

  def update(self):
    MoveableObject.update(self)

    pos = self.rect.x + self.level.world_shift

    frame = int(pos // 10) % len(self.images_list)
    self.image = self.images_list[frame]
    
    
  def set_in_motion(self, dist):
    if dist < 0:
      self.direction = LEFT
      self.images_list = self.images_run_l
    else:
      self.direction = RIGHT
      self.images_list = self.images_run_r

    self.speed_x = dist if self.hands_empty else 0.75 * dist

  def move_y(self):
    MoveableObject.move_y(self)

    if not self.hands_empty:
      if abs(self.rect.y - self.holded_object.rect.y) > self.rect.height * 0.75:
        self.drop_holded()

  def jump(self, speed):
    self.rect.y += 2
    platform_collisions = pygame.sprite.spritecollideany(self, self.level.platforms)
    door_collisions = pygame.sprite.spritecollideany(self, self.level.doors)
    cube_collisions = pygame.sprite.spritecollideany(self, self.level.cubes)
    button_collisions = pygame.sprite.spritecollideany(self, self.level.buttons)
    self.rect.y -= 2

    if (platform_collisions or cube_collisions or button_collisions or door_collisions):
      if self.hands_empty:
        self.speed_y = speed
      else:
        self.speed_y = 0.7 * speed
        if self.rect.y == self.holded_object.rect.y:
          self.holded_object.speed_y = 0.7 * speed

    if self.direction == RIGHT:
      self.images_list = self.images_jump_r
    else:
      self.images_list = self.images_jump_l

  def stop(self):
    MoveableObject.stop(self)
    if self.direction == RIGHT:
      self.images_list = self.images_idle_r
    else:
      self.images_list = self.images_idle_l


  def on_goal(self):
    return pygame.sprite.spritecollideany(self, self.level.exit) is not None

  def horizontal_collision_handler(self, block_collisions, with_moveable = False):
    if with_moveable:
      if not self.hands_empty:
        if len([b for b in block_collisions if b.order_number != self.holded_object.order_number]) > 0:
          self.holded_object.stop()
        else:
          self.holded_object.speed_x = self.speed_x
      for block in block_collisions:
      # if self.hands_empty or block.order_number is not self.holded_object.order_number:
        if self.speed_x > 0:
          self.rect.right = block.rect.left
        elif self.speed_x < 0:
          self.rect.left = block.rect.right
        block.speed_x = 0.4 * self.speed_x
    else:
      MoveableObject.horizontal_collision_handler(self, block_collisions, with_moveable)

  def vertical_collision_handler(self, block_collisions, with_moveable = False):
    MoveableObject.vertical_collision_handler(self, block_collisions, with_moveable)
    if self.speed_y == 0:
      if self.direction == RIGHT:
        if self.speed_x == 0:
          self.images_list = self.images_idle_r
        else:
          self.images_list = self.images_run_r
      else:
        if self.speed_x == 0:
          self.images_list = self.images_idle_l
        else:
          self.images_list = self.images_run_l

  def try_pickup(self):
    delta = self.rect.width / 3
    if self.direction is LEFT:
      self.rect.x -= delta
    self.rect.width += delta
    cubes_nearby = sorted(pygame.sprite.spritecollide(self, self.level.cubes, False), key = lambda c: (c.rect.y, abs(c.rect.x - self.rect.x)))
    self.rect.width -= delta
    if self.direction is LEFT:
      self.rect.x += delta

    if len(cubes_nearby) > 0:
      self.hands_empty = False
      self.holded_object = cubes_nearby[0]
      self.holded_object.holded = True
      self.holded_object.holded_by = self
      
      if self.holded_object.direction is not self.direction:
        self.holded_object.flip()
      self.holded_object.rect.top = self.rect.top


  def drop_holded(self):
    self.holded_object.holded = False
    self.holded_object.holded_by = None
    self.holded_object.movement_key_pressed = False
    self.hands_empty = True
    self.holded_object = None
  
