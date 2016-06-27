from configuration import *
from Platform import *
from Portal import *
from Items import *
from Button import *
from Door import *
from Exit import *
import pygame

class Level():

  def __init__(self, player, player2 = None):
    self.platforms = pygame.sprite.Group()
    self.cubes = pygame.sprite.Group()
    self.buttons = pygame.sprite.Group()
    self.doors = pygame.sprite.Group()
    self.player = player
    self.player2 = player2
    self.portal_blue = pygame.sprite.GroupSingle()
    self.portal_orange = pygame.sprite.GroupSingle()
    self.exit = pygame.sprite.GroupSingle()

    self.world_shift = 0
    
    self.background = pygame.transform.scale(pygame.image.load(bg_image_default), window_size).convert()
    self.bg_1_x = -100
    self.bg_2_x = screen_x - 100

  def update(self):
    self.platforms.update()
    self.cubes.update()
    self.buttons.update()
    self.doors.update()
    self.portal_blue.update()
    self.portal_orange.update()
    self.exit.update()

  def draw(self, screen):
    
    screen.blit(self.background, (self.bg_1_x, 0))
    screen.blit(self.background, (self.bg_2_x, 0))

    self.platforms.draw(screen)
    self.cubes.draw(screen)
    self.buttons.draw(screen)
    self.doors.draw(screen)

    if self.portal_blue is not None:
      self.portal_blue.draw(screen)
    if self.portal_orange is not None:
      self.portal_orange.draw(screen)

    if self.exit is not None:
      self.exit.draw(screen)

  def shift_world(self, shift_x):
    
    if shift_x > 0:
      self.bg_1_x += 1
      self.bg_2_x += 1
      if self.bg_1_x > screen_x:
        self.bg_1_x = -screen_x
      if self.bg_2_x > screen_x:
        self.bg_2_x = -screen_x

    if shift_x < 0:
      self.bg_1_x -= 1
      self.bg_2_x -= 1
      if self.bg_1_x < -screen_x:
        self.bg_1_x = screen_x
      if self.bg_2_x < -screen_x:
        self.bg_2_x = screen_x

    self.world_shift += shift_x

    if self.player2 is not None:
      self.player2.rect.x += shift_x

    for platform in self.platforms:
      platform.rect.x += shift_x

    for cube in self.cubes:
      if not cube.holded:
        cube.rect.x += shift_x
    
    for button in self.buttons:
      button.rect.x += shift_x

    for door in self.doors:
      door.rect.x += shift_x

    if self.portal_blue.sprite is not None:
      self.portal_blue.sprite.rect.x += shift_x
    if self.portal_orange.sprite is not None:
      self.portal_orange.sprite.rect.x += shift_x

    if self.exit.sprite is not None:
      self.exit.sprite.rect.x += shift_x

  def open_portal(self, click, is_blue, use_second_player = False):
    player = self.player2 if use_second_player else self.player
    portal_gun_point = (player.rect.right, player.rect.centery) if player.direction is RIGHT else (player.rect.left, player.rect.centery)
    
    # The logic in the key of sorted() function below is off a bit. Consider finding a better condition.
    platforms_in_the_way = sorted([p for p in self.platforms if p.portal_supporting and p.intersection(portal_gun_point, click) is not None], key = lambda p: abs(p.intersection_point[1] - portal_gun_point[1]))
    obstacles = [d for d in self.doors if d.intersection(portal_gun_point, click)]
    can_open = len(platforms_in_the_way) > 0 and len(obstacles) == 0

    if can_open:
      platform_for_portal = platforms_in_the_way[0]
      
      direction = platform_for_portal.get_portal_direction()
      
      if direction is RIGHT or direction is LEFT:
        width = int(portal_width * 0.2)
        height = platform_for_portal.rect.height if platform_for_portal.rect.height < portal_height else portal_height
      else:
        width = platform_for_portal.rect.width if platform_for_portal.rect.width < portal_width else portal_width
        height = int(portal_width * 0.2)

      (portal_x, portal_y) = platform_for_portal.intersection_point

      x = portal_x - 0.5 * width
      y = portal_y - 0.5 * height

      if width > int(portal_width * 0.4) or height > int(portal_height * 0.4):

        portal = Portal_opened(width, height, is_blue, direction)
        portal.rect.x = x
        portal.rect.y = y
        
        if is_blue:
          if self.portal_orange.sprite is None or not pygame.sprite.collide_rect(portal, self.portal_orange.sprite):
            self.portal_blue.sprite = portal
        else:
          if self.portal_blue.sprite is None or not pygame.sprite.collide_rect(portal, self.portal_blue.sprite):
            self.portal_orange.sprite = portal
          
      
class Level_01(Level):

  def __init__(self, player, player2 = None):
    Level.__init__(self, player, player2)

    self.background = pygame.transform.scale(pygame.image.load(bg_image_01), window_size).convert()
    
    # every platform: width, height, x, y
    level = [
             [20, screen_y, -300, 0],
             [1900, 20, -300, 0],
             [1900, 20, -300, screen_y - 20],
             [1210, 10, 50, 500],
             [10, 130, 700, 400],
             [1210, 10, 50, 280],
             [10, 310, 1400, 180],
             [exit_width + 20, int(0.3 * screen_y), 1580, 0],
             [exit_width + 20, int(0.7 * screen_y - exit_height), 1580, int(0.3 * screen_y + exit_height)]
             ]

    self.left_border = level[0][2]

    for platform in level:
      block = Platform(platform[0], platform[1])

      block.rect.x = platform[2]
      block.rect.y = platform[3]

      self.platforms.add(block)

    cubes = [(60, 450),
             (100, 510)]

    for (i, cube) in enumerate(cubes):
      block = Cube(i)

      block.rect.x = cube[0]
      block.rect.y = cube[1]

      block.level = self

      self.cubes.add(block)

    buttons = [
               (100, 500),
       #        (500, 280)
               ]
    doors = [
             (200, 500),
        #     (1570, 0.50 * screen_y)            
            ]

    for (i, button) in enumerate(buttons):
      block = Button()

      block.rect.x = button[0]
      block.rect.bottom = button[1]

      door = Door()

      door.rect.x = doors[i][0]
      door.rect.bottom = doors[i][1]

      door.button = block

      block.door = door

      block.level = self

      self.doors.add(door)
      self.buttons.add(block)

    self.exit.sprite = Exit()
    self.exit.sprite.rect.x = 1600
    self.exit.sprite.rect.y = 0.3 * screen_y
