import string
import re

import pygame
from pygame.locals import *

from configuration import *

incorrect_input = list("Enter a valid IP!")

def get_key():
  while True:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def draw_input_field(screen, content):
  font = pygame.font.SysFont(u'ubuntumono', text_size_menu)
  pygame.draw.rect(screen, BLACK,
        (screen_x_center - input_field_x_shift, screen_y_center, input_field_w, text_size_menu + 5), 0)
  pygame.draw.rect(screen, WHITE,
        (screen_x_center - input_field_x_shift - 2, screen_y_center, input_field_w + 4, text_size_menu + 6), 1)
  if len(content) != 0:
    screen.blit(font.render(content, 1, WHITE),
        (screen_x_center - input_field_x_shift + 6, screen_y_center + 1))
  pygame.display.flip()

def ask(start_text = ""):
  screen = pygame.display.get_surface()
  pygame.font.init()
  current_string = list(start_text)
  draw_input_field(screen, "".join(current_string))
  while True:
    inkey = get_key()
    if current_string == incorrect_input:
      current_string = []
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      pattern = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}$")
      s = "".join(current_string)
      if pattern.match(s):
        return s
      else:
        current_string = incorrect_input
    elif inkey == K_ESCAPE or inkey == K_q:
      return None
    elif inkey != 47 and inkey > 45 and inkey < 58:
      current_string.append(chr(inkey))
    draw_input_field(screen, "".join(current_string))

def ask_f(start_text = ""):
  screen = pygame.display.get_surface()
  pygame.font.init()
  current_string = list(start_text)
  draw_input_field(screen, "".join(current_string))
  while True:
    inkey = get_key()
    if current_string == incorrect_input:
      current_string = []
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      return "".join(current_string) + ".py"
    elif inkey == K_ESCAPE or inkey == K_q:
      return None
    elif inkey < 147:
      current_string.append(chr(inkey))
    draw_input_field(screen, "".join(current_string))
