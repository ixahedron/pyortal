import sys
import pygame
from pygame.locals import *
import Textfield

from configuration import *
from Platform import *
from Items import *
from Button import *
from Door import *
from Exit import *

# Initialise pygame
def initialise():
  pygame.init()
  
  if not pygame.display.get_init():
    pygame.display.init()

  if not pygame.font.get_init():
    pygame.font.init()

  window = pygame.display.set_mode(window_size)

  pygame.display.set_caption(game_title)

def map_editor():
  screen = pygame.display.get_surface()
  me = Map_editor()
  me.draw(screen)
  me.edit()

class Map_editor():

  def __init__(self):
    self.platforms = pygame.sprite.Group()
    self.cubes = pygame.sprite.Group()
    self.doors = pygame.sprite.Group()
    self.buttons = pygame.sprite.Group()
    self.exit = pygame.sprite.GroupSingle()

    self.background = pygame.transform.scale(pygame.image.load(bg_image_default), window_size).convert() # perhaps if I find the image
    # self.background = pygame.Surface(window_size)
    # self.background.fill(BLACK)

    self.shift_x = 0
    self.shift_y = 0

    self.second_click_awaited = False
    self.cube_index = 0
    self.current_coordinate = (0, 0)
    self.current_action = "p"

  def update(self):
    self.platforms.update()
    self.cubes.update()
    self.doors.update()
    self.buttons.update()
    self.exit.update()

  def draw(self, screen):
    
    screen.blit(self.background, (0, 0))

    self.platforms.draw(screen)
    self.cubes.draw(screen)
    self.doors.draw(screen)
    self.buttons.draw(screen)
    self.exit.draw(screen)

  def screen_shift(self, shift_x, shift_y):
    
    self.shift_x += shift_x
    self.shift_y += shift_y

    for platform in self.platforms:
      platform.rect.x += shift_x
      platform.rect.y += shift_y

    for cube in self.cubes:
      cube.rect.x += shift_x
      cube.rect.y += shift_y
    
    for button in self.buttons:
      button.rect.x += shift_x
      button.rect.y += shift_y

    for door in self.doors:
      door.rect.x += shift_x
      door.rect.y += shift_y

    if self.exit.sprite is not None:
      self.exit.sprite.rect.x += shift_x
      self.exit.sprite.rect.y += shift_y

    if self.second_click_awaited:
      self.current_coordinate = [x + y for (x, y) in zip(self.current_coordinate, (shift_x, shift_y))]


  def edit(self):
    screen = pygame.display.get_surface()
    pygame.display.update()
    
    actions = {"p" : self.place_platform, "n" : lambda: self.place_platform(True), "c" : self.place_cube, "b" : self.place_button, "d" : self.place_door, "e" : self.place_exit, "r" : self.remove_sprite}
    
    not_chosen = True
    second_click_awaited = False
    
    while not_chosen:
      for event in pygame.event.get():
        if event.type == QUIT:
          not_chosen = False

        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE or event.key == K_q:
            not_chosen = False

          elif event.key == K_UP:
            self.screen_shift(0, 100)

          elif event.key == K_DOWN:
            self.screen_shift(0, -100)

          elif event.key == K_RIGHT:
            self.screen_shift(-100, 0)

          elif event.key == K_LEFT:
            self.screen_shift(100, 0)

          elif event.key == K_p:
            self.current_action = "p"

          elif event.key == K_n:
            self.current_action = "n"

          elif event.key == K_c:
            self.current_action = "c"

          elif event.key == K_b:
            self.current_action = "b"

          elif event.key == K_d:
            self.current_action = "d"

          elif event.key == K_e:
            self.current_action = "e"

          elif event.key == K_r:
            self.current_action = "r"

          elif event.key == K_s:
            filename = Textfield.ask_f("level")
            self.save(filename)
            # not_chosen = False

        elif event.type == MOUSEBUTTONUP:
          if event.button == 1:
            actions.get(self.current_action)()

        self.draw(screen)
        pygame.display.update()
      pygame.time.wait(8)
    pygame.display.quit()
    sys.exit()

  def place_platform(self, black = False):
    if self.second_click_awaited:
      pos = pygame.mouse.get_pos()
      self.second_click_awaited = False

      p_type = NonPortalPlatform if black else Platform

      p = p_type(abs(pos[0] - self.current_coordinate[0]), abs(pos[1] - self.current_coordinate[1]))
      p.rect.x = min(pos[0], self.current_coordinate[0])
      p.rect.y = min(pos[1], self.current_coordinate[1])

      self.platforms.add(p)
    else:
      self.current_coordinate = pygame.mouse.get_pos()
      self.second_click_awaited = True
    
  def place_cube(self):
    pos = pygame.mouse.get_pos()

    p = Cube(self.cube_index)
    p.rect.x = pos[0]
    p.rect.y = pos[1]

    self.cube_index += 1
    self.cubes.add(p)
    
  def place_button(self):
    pos = pygame.mouse.get_pos()

    p = Button()
    p.rect.x = pos[0]
    p.rect.bottom = pos[1]

    self.buttons.add(p)
    
    self.current_action = "d"

  def place_door(self):
    pos = pygame.mouse.get_pos()

    p = Door()
    p.rect.x = pos[0]
    p.rect.bottom = pos[1]

    self.doors.add(p)
    
    self.current_action = "b"
  
  def place_exit(self):
    pos = pygame.mouse.get_pos()

    p = Exit()
    p.rect.x = pos[0]
    p.rect.y = pos[1]

    self.exit.sprite = p

  def remove_sprite(self):
    pos = pygame.mouse.get_pos()

    sprites = self.platforms.sprites() + self.cubes.sprites() + self.buttons.sprites() + self.doors.sprites() + self.exit.sprites()

    for p in sprites:
      if p.rect.collidepoint(pos):
        p.kill()

  def open_map(self, filename):
    l = __import__(filename)

  def save(self, filename):
    left = 0
    right = screen_x
    top = 0
    bottom = screen_y

    p = []
    n = []
    c = []
    b = []
    d = []

    for platform in self.platforms:
      if platform.rect.left - self.shift_x < left:
        left = platform.rect.left - self.shift_x
      if platform.rect.right - self.shift_x > right:
        right = platform.rect.right - self.shift_x
      if platform.rect.top - self.shift_y < top:
        top = platform.rect.top - self.shift_y
      if platform.rect.bottom > bottom:
        bottom = platform.rect.bottom - self.shift_y
      if platform.portal_supporting:
        p.append([platform.rect.width, platform.rect.height, platform.rect.x - self.shift_x, platform.rect.y - self.shift_y])
      else:
        n.append([platform.rect.width, platform.rect.height, platform.rect.x - self.shift_x, platform.rect.y - self.shift_y])

    for cube in self.cubes:
      c.append((cube.rect.x - self.shift_x, cube.rect.y - self.shift_y))

    for button in self.buttons:
      b.append((button.rect.x - self.shift_x, button.rect.bottom - self.shift_y))

    for door in self.doors:
      d.append((door.rect.x - self.shift_x, door.rect.bottom - self.shift_y))

    with open(filename, 'w') as f:
      f.write("from configuration import *\n")
      f.write("\n")

      f.write("# every platform: width, height, x, y\n")
      f.write("level = ")
      f.write(repr(p) + "\n")
      f.write("\n")

      f.write("black_platforms = ")
      f.write(repr(n) + "\n")
      f.write("\n")

      f.write("left_border = " + str(left) + "\n")
      f.write("right_border = " + str(right) + "\n")
      f.write("top_border = " + str(top) + "\n")
      f.write("bottom_border = " + str(bottom) + "\n")
      f.write("\n")

      f.write("cubes = ")
      f.write(repr(c) + "\n")
      f.write("\n")

      f.write("buttons = ")
      f.write(repr(b) + "\n")
      f.write("\n")

      f.write("doors = ")
      f.write(repr(d) + "\n")
      f.write("\n")

      if self.exit.sprite is not None:
        f.write("exit_x = " + str(self.exit.sprite.rect.x - self.shift_x) + "\n")
        f.write("exit_y = " + str(self.exit.sprite.rect.y - self.shift_y) + "\n")


if __name__ == "__main__":
  initialise()
  map_editor()
  pygame.display.quit()
  sys.exit()
