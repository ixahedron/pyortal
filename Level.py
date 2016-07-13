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
    self.world_shift_y = 0
    
    self.background = pygame.transform.scale(pygame.image.load(bg_image_default), window_size).convert()
    self.bg_1_x = -100
    self.bg_2_x = screen_x - 100

  def init_platforms(self, level, are_blacks = False):
    p_type = NonPortalPlatform if are_blacks else Platform

    for platform in level:
      block = p_type(platform[0], platform[1])

      block.rect.x = platform[2]
      block.rect.y = platform[3]

      self.platforms.add(block)

  def init_cubes(self, cubes):
    for (i, cube) in enumerate(cubes):
      block = Cube(i)

      block.rect.x = cube[0]
      block.rect.y = cube[1]

      block.level = self

      self.cubes.add(block)

  def init_buttons(self, buttons, doors):
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

  def shift_world(self, shift_x, shift_y = 0):
    
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
    self.world_shift_y += shift_y

    if self.player2 is not None:
      self.player2.rect.x += shift_x
      self.player2.rect.y += shift_y

    for platform in self.platforms:
      platform.rect.x += shift_x
      platform.rect.y += shift_y

    for cube in self.cubes:
      if not cube.holded:
        cube.rect.x += shift_x
        cube.rect.y += shift_y
    
    for button in self.buttons:
      button.rect.x += shift_x
      button.rect.y += shift_y

    for door in self.doors:
      door.rect.x += shift_x
      door.rect.y += shift_y

    if self.portal_blue.sprite is not None:
      self.portal_blue.sprite.rect.x += shift_x
      self.portal_blue.sprite.rect.y += shift_y
    if self.portal_orange.sprite is not None:
      self.portal_orange.sprite.rect.x += shift_x
      self.portal_orange.sprite.rect.y += shift_y

    if self.exit.sprite is not None:
      self.exit.sprite.rect.x += shift_x
      self.exit.sprite.rect.y += shift_y

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
          
      
class Level_M_01(Level):

  def __init__(self, player, player2 = None):
    Level.__init__(self, player, player2)

    # every platform: width, height, x, y
    
    # Level 1
##
##    level = [
##                  (600, 	10,	 	0,	 	0,		True),
##                  (10,	800, 	0,	 	0, 		False),
##                  (10, 	200, 	600, 	0, 		False),
##                  (10, 	400, 	600, 	600,	False),
##                  (600, 	10,		0,		1000,	False),
##
##                  (10, 	200,	1000,	0,		False),
##                  (600,	10,		1000,	0,		False),
##                  (10,	600,	1000,	400,	False),
##                  (600, 	10, 	1000,	1000,	True),
##                  (10,	1000,	1600,	0,		False),
##                  (400,	200,	1000,	200,	True)      
##          ]
##
##    # Level 2
##
##    level = [
##                          
##          ]
##
##    # Level 3
##
##    level = [
##                          (1200,	10,		0,		0,		False),
##                  (10,	200,	0,		0,		True),
##                  (200,	10,		0,		200,	False),
##                  (10,	300,	200,	200,	True),
##                  (200,	10,		0,		500,	False),
##                  (10,	400,	0,		500,	True),
##                  (800,	10,		0,		700,	False),
##                  (600,	100,	0,		900,	False),
##                  (10,	300,	1000,	700,	False),
##                  (10,	100,	990,	850,	True),
##                  (10,	200,	1000,	500,	True),
##                  (250,	100,	950,	400,	False),
##                  (10,	400,	1200,	0,		False),
##                  (400,	10,		800,	200, 	False)
##          ]
##
##    # Level 4
##
##    level = [
##                  (1400,	10,		0,		0,		False),
##                  (10,	600,	1400,	0,		True),
##                  (10,	1000,	0,		0,		False),
##                  (500,	10,		0,		300,	False),
##                  (800,	10,		0,		600,	False),
##                  (200,	10,		300,	595,	True),
##                  (400,	10,		0,		1000,	False)          
##          ]
##
##    # Level 5
##
##    level = [
##                  (200,	10,		100,	0,		False),
##                  (10,	200,	0,		100,	True),
##                  (400,	10,		100,	700,	True),
##                  (400,	10,		900,	0,		True),
##                  (400,	10,		800,	700,	False),
##                  (300,	10,		1400,	200,	False)
##          ]
##
##    # Level 6
##
##    level = [
##                  (10,	200,	0,		0,		False),
##                  (300,	10,		0,		0,		True),
##                  (300,	10,		0,		500,	False),
##                  (900,	10,		0,		800,	False),
##                  (300,	300,	600,	300,	False)   
##          ]
##
##    # MP Level 1
##
##    level = [
##                  (500,	10,		0,		0,		True),
##                  (1200,	10,		500,	0,		False),
##                  (10,	400,	1700,	0,		True),
##                  (200,	400,	1500,	400,	False),
##                  (200,	10,		1300,	800,	False),
##                  (200,	10,		1100,	800,	True),
##                  (800,	10,		300,	800,	False),
##                  (10,	200,	300,	400,	False),
##
##                  (200,	200,	300,	200,	False),
##                  (200,	400,	700,	200,	False),
##                  (200,	400,	1100,	200,	False),
##                  (200,	200,	300,	600,	False),
##
##                  (200,	800,	0,		200,	False),
##                  (2800,	10,		200,	1000,	False),
##                  (1200,	10,		1700,	800,	False)
##          ]
##    # MP Level 2
##
    level = [
              [20, screen_y, -300, 0],
              (2300, 	10, 	-300,	0, 		False),
              (500, 	10, 	400,	300, 		False),
              (600, 	10, 	-300,	300, 		False),
              (20,      100,    500,    310,            False),
              (20,      130,    800,    10,             False),
              (20,      100,    1300,   310,            False),
              (20,      130,    1300,    10,             False),
              (600, 	10, 	1200,	300, 		False),
              (2300, 	30, 	-300,      570,	        False),    
              [exit_width + 20, int(0.3 * screen_y), 1580, 0],
              [exit_width + 20, int(0.7 * screen_y - exit_height), 1580, int(0.3 * screen_y + exit_height)]
          ]

    cubes = [
            (600, 290),
            (600, 550),
            (1100, 550),
            (1500, 550)
            ]


    buttons = [
               (500, 305),
               (800, 575),
               (1000, 575),
               (1400, 575)
              ]
    doors = [
              (500, 572),
              (800, 300),
              (1300, 572),
              (1300,300)
            ]
    
##    # MP Level 3
##
##    level = [
##                  (900,	200,	0,		0,		False),
##                  (600,	10,		900,	0,		False),
##                  (10,	200,	1500,	0,		True),
##                  (100,	210,	1200,   200,	True),
##                  (10,	400,	1500,	200,	False),
##                  (600,	100,	1500,	600,	False),
##                  (600,	100,	1500,	800,	False),
##                  (200,	400,	1200,	900,	False),
##                  (500,	200,	0,		1200,	False),
##                  (10,	1200,	0,		400,	False),
##                  (200,	10,		0,		400,	True),
##                  (300,	10,		0,		600,	True),
##                  (10,	200,	300,	400,	False),
##                  (900,	10,		300,	400,	False)
##        ]

            

    self.left_border = level[0][2]
    self.top_border = 0
    self.bottom_border = screen_y


    self.init_platforms(level)
    self.init_cubes(cubes)
    self.init_buttons(buttons, doors)

    self.exit.sprite = Exit()
    self.exit.sprite.rect.x = 1600
    self.exit.sprite.rect.y = 0.3 * screen_y


class Level_01(Level):

  def __init__(self, player, player2 = None):
    Level.__init__(self, player, player2)

    import level_01 as l

    self.init_platforms(l.level)
    self.init_platforms(l.black_platforms, True)
    self.init_cubes(l.cubes)
    self.init_buttons(l.buttons, l.doors)
    
    self.left_border = l.left_border
    self.top_border = l.top_border
    self.bottom_border = l.bottom_border

    self.exit.sprite = Exit()
    self.exit.sprite.rect.x = l.exit_x
    self.exit.sprite.rect.y = l.exit_y
