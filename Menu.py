import sys
import pygame
from pygame.locals import *
import Textfield

from configuration import *
import Singleplayer
import Multiplayer

# Initialise pygame
def initialise():
  pygame.init()
  
  if not pygame.display.get_init():
    pygame.display.init()

  if not pygame.font.get_init():
    pygame.font.init()

  window = pygame.display.set_mode(window_size)

  pygame.display.set_caption(game_title)

def menu():
  menu = change_menu_options({1: "Multiplayer", 2: "Singleplayer", 0: "Exit"})
  return menu.controls()

def change_menu_options(options_dict):
  screen = pygame.display.get_surface()
  menu = Menu(options_dict)
  menu.draw(screen)
  return menu


class Menu():

  def __init__(self, options_dict):
    self.options = pygame.sprite.Group()

    for (offset, option) in options_dict.items():
      opt = Option(option)
      opt.rect.y = screen_y - 50 - (offset+1) * 100
      self.options.add(opt)

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
              if option.text == "Singleplayer" and option.rect.collidepoint(pygame.mouse.get_pos()):
                return Singleplayer.main
              elif option.text == "Multiplayer" and option.rect.collidepoint(pygame.mouse.get_pos()):
                self = change_menu_options({2: "Create a game", 1: "Connect to a game", 0: "Return"})
                return self.controls()
              elif option.text == "Create a game" and option.rect.collidepoint(pygame.mouse.get_pos()):
                return lambda: Multiplayer.main(1)
              elif option.text == "Connect to a game" and option.rect.collidepoint(pygame.mouse.get_pos()):
                self = change_menu_options({2: "Enter the other player's IP:"})
                host = Textfield.ask(mp_host)
                if host is None:
                  self = change_menu_options({2: "Create a game", 1: "Connect to a game", 0: "Return"})
                  return self.controls()
                else:
                  return lambda: Multiplayer.main(2, host)
              elif option.text == "Return" and option.rect.collidepoint(pygame.mouse.get_pos()):
                self = change_menu_options({1: "Multiplayer", 2: "Singleplayer", 0: "Exit"})
                return self.controls()
              elif option.text == "Exit" and option.rect.collidepoint(pygame.mouse.get_pos()):
                not_chosen = False
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
    self.rect.x = screen_x / 2 - width / 2 - 2


if __name__ == "__main__":
  initialise()
  if use_menu:
    mode_main = menu()
    mode_main()
  else:
    Singleplayer.main()
  pygame.display.quit()
  sys.exit()
