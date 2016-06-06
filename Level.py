from configuration import *
from Platform import *
from Portal import *
from Exit import *
import pygame

class Level():

  def __init__(self, player):
    self.platforms = pygame.sprite.Group()
    self.player = player
    self.portal_blue = pygame.sprite.GroupSingle()
    self.portal_orange = pygame.sprite.GroupSingle()
    self.exit = pygame.sprite.GroupSingle()

    self.world_shift = 0
    
    self.background = pygame.transform.scale(pygame.image.load(bg_image_default), window_size).convert()
    self.bg_1_x = -100
    self.bg_2_x = screen_x - 100

  def update(self):
    self.platforms.update()
    self.portal_blue.update()
    self.portal_orange.update()
    self.exit.update()

  def draw(self, screen):
    
    screen.blit(self.background, (self.bg_1_x, 0))
    screen.blit(self.background, (self.bg_2_x, 0))

    self.platforms.draw(screen)

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

    for platform in self.platforms:
      platform.rect.x += shift_x

    if self.portal_blue.sprite is not None:
      self.portal_blue.sprite.rect.x += shift_x
    if self.portal_orange.sprite is not None:
      self.portal_orange.sprite.rect.x += shift_x

    if self.exit.sprite is not None:
      self.exit.sprite.rect.x += shift_x

  def open_portal(self, click, is_blue):

    if self.player.direction == RIGHT:
      portal_gun_point = (self.player.rect.x + self.player.rect.width, self.player.rect.y + 0.5 * self.player.rect.height)
    else:
      portal_gun_point = (self.player.rect.x, self.player.rect.y + 0.5 * self.player.rect.height)
    
    # The logic in the key of sorted() function below is off a bit. Consider finding a better condition.
    platforms_in_the_way = sorted([p for p in self.platforms if p.intersection(portal_gun_point, click) is not None], key = lambda p: abs(p.intersection_point[1] - portal_gun_point[1]))
    can_open = len(platforms_in_the_way) > 0

    if can_open:
      platform_for_portal = platforms_in_the_way[0]
      
      width = platform_for_portal.rect.width if platform_for_portal.rect.width < portal_width else portal_width
      height = platform_for_portal.rect.height if platform_for_portal.rect.height < portal_height else portal_height

      (portal_x, portal_y) = platform_for_portal.intersection_point

      x = portal_x - 0.5 * width
      y = portal_y - 0.5 * height

      direction = platform_for_portal.get_portal_direction()
        
      if is_blue:
        self.portal_blue.sprite = Portal_opened(width, height, is_blue, direction)
        
        self.portal_blue.sprite.rect.x = x
        self.portal_blue.sprite.rect.y = y
    
      else:
        self.portal_orange.sprite = Portal_opened(width, height, is_blue, direction)
        
        self.portal_orange.sprite.rect.x = x
        self.portal_orange.sprite.rect.y = y
  
      
class Level_01(Level):

  def __init__(self, player):
    Level.__init__(self, player)

    self.background = pygame.transform.scale(pygame.image.load(bg_image_01), window_size).convert()
    
    # every platform: width, height, x, y
    level = [[1210, 10, 50, 500],
             [10, 130, 700, 400],
             [1210, 10, 50, 280],
             [10, 310, 1400, 180],
             [exit_width + 20, int(0.3 * screen_y), 1580, 0],
             [exit_width + 20, int(0.7 * screen_y - exit_height), 1580, int(0.3 * screen_y + exit_height)]]

    for platform in level:
      block = Platform(platform[0], platform[1])

      block.rect.x = platform[2]
      block.rect.y = platform[3]

      block.player = self.player
      self.platforms.add(block)

    self.exit.sprite = Exit()
    self.exit.sprite.rect.x = 1600
    self.exit.sprite.rect.y = 0.3 * screen_y