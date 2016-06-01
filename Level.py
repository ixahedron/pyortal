from configuration import *
from Platform import *
from Portal import *
import pygame

class Level():

  def __init__(self, player):
    self.platforms = pygame.sprite.Group()
    self.player = player
    self.portal_blue = pygame.sprite.GroupSingle()
    self.portal_orange = pygame.sprite.GroupSingle()

    self.world_shift = 0
    
    self.background = pygame.transform.scale(pygame.image.load(bg_image_default), window_size).convert()
    self.bg_1_x = -100
    self.bg_2_x = screen_x - 100

  def update(self):
    self.platforms.update()

  def draw(self, screen):
    
    #screen.fill(BLUE)
    screen.blit(self.background, (self.bg_1_x, 0))
    screen.blit(self.background, (self.bg_2_x, 0))

    self.platforms.draw(screen)

    if self.portal_blue is not None:
      self.portal_blue.draw(screen)
    if self.portal_orange is not None:
      self.portal_orange.draw(screen)

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

  def open_blue_portal(self, (click_x, click_y)):

    platform_for_portal = [p for p in self.platforms if p.rect.collidepoint(click_x, click_y)]
    can_open = len(platform_for_portal) > 0

    if can_open:
      width = platform_for_portal[0].rect.width + 4 if platform_for_portal[0].rect.width < portal_width else portal_width
      height = platform_for_portal[0].rect.height + 4 if platform_for_portal[0].rect.height < portal_height else portal_height

      self.portal_blue.sprite = Portal_blue(width, height)
  
      x = click_x - 0.5 * self.portal_blue.sprite.rect.width
      y = click_y - 0.5 * self.portal_blue.sprite.rect.height
    
      self.portal_blue.sprite.rect.x = x
      self.portal_blue.sprite.rect.y = y

  def open_orange_portal(self, (click_x, click_y)):
    
    platform_for_portal = [p for p in self.platforms if p.rect.collidepoint(click_x, click_y)]
    can_open = len(platform_for_portal) > 0

    if can_open:
      width = platform_for_portal[0].rect.width + 4 if platform_for_portal[0].rect.width < portal_width else portal_width
      height = platform_for_portal[0].rect.height + 4 if platform_for_portal[0].rect.height < portal_height else portal_height

      self.portal_orange.sprite = Portal_orange(width, height)
  
      x = click_x - 0.5 * width
      y = click_y - 0.5 * height
    
      self.portal_orange.sprite.rect.x = x
      self.portal_orange.sprite.rect.y = y

      
class Level_01(Level):

  def __init__(self, player):
    Level.__init__(self, player)

    self.level_limit = -1000
    
    self.background = pygame.transform.scale(pygame.image.load(bg_image_01), window_size).convert()
    
    # every platform: width, height, x, y
    level = [[1210, 10, 100, 500],
             [10, 130, 800, 400],
             [1210, 10, 100, 280],
             [10, 310, 1500, 180]]

    for platform in level:
      block = Platform(platform[0], platform[1])

      block.rect.x = platform[2]
      block.rect.y = platform[3]

      block.player = self.player
      self.platforms.add(block)
