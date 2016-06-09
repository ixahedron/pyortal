from configuration import *

import sys
import pygame
from pygame.locals import *

if not pygame.display.get_init():
  pygame.display.init()

if not pygame.font.get_init():
  pygame.font.init()

class Menu():

  def __init__(self, options_list):
    self.options = pygame.sprite.Group()

    for option in options_list:
      self.options.add(Option(option))

    for (i, option) in enumerate(reversed(list(self.options))):
      option.rect.y = screen_y - 100 - (i+1) * 100

    # self.background = pygame.transform.scale(pygame.image.load(menu_image), window_size).convert() # perhaps if I find the image
    self.background = pygame.Surface(window_size)
    self.background.fill(BLACK)


    logo = pygame.transform.scale(pygame.image.load(logo_menu), (int(screen_x * 0.75), int(screen_y * 0.25))).convert()
    self.background.blit(logo, (int((screen_x * 0.25) / 2), int(screen_y * 0.15)))

  def update(self):
    self.options.update()

  def draw(self, screen):
    
    screen.blit(self.background, (0, 0))

    self.options.draw(screen)

  def controls(self):
    pygame.display.update()
    not_chosen = True
    while not_chosen:
      for event in pygame.event.get():
        if event.type == QUIT:
          not_chosen = False

        if event.type == KEYDOWN:
          if event.key == K_ESCAPE or event.key == K_q:
            not_chosen = False

        if event.type == MOUSEBUTTONUP:
          if event.button == 1:
            for option in self.options:
              if option.text == "Start" and option.rect.collidepoint(pygame.mouse.get_pos()):
                return 0
              elif option.text == "Exit" and option.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.display.quit()
                sys.exit()
        pygame.display.update()
      pygame.time.wait(8)
    pygame.display.quit()
    sys.exit()

class Option(pygame.sprite.Sprite):
  
  def __init__(self, text):
    pygame.sprite.Sprite.__init__(self)

    bg = BLACK

    self.font = pygame.font.SysFont(u'ubuntumono', text_size_menu)
    self.text = text
    self.textr = self.font.render(text, 1, WHITE, bg)

    width = self.textr.get_width()
    height = self.textr.get_height()
    
    self.image = pygame.Surface((width + 40, height + 40))
    self.image.fill(bg)

    self.image.blit(self.textr, (20, 20))

    self.rect = self.image.get_rect()
    self.rect.x = screen_x / 2 - width / 2 - 20
