import pygame
import sys
from pygame.locals import *

from configuration import *
from Player import *
from Level import *

# Initialise mixer

# Initialise pygame
pygame.init()

window = pygame.display.set_mode(window_size)

pygame.display.set_caption(game_title)

screen = pygame.display.get_surface()

clock = pygame.time.Clock()

#Initialise player
player = Player()
player.rect.x = player_start_x
player.rect.y = player_start_y

# Initialise levels
levels = []
levels.append(Level_01(player))

current_level_number = 0
current_level = levels[current_level_number]

player.level = current_level

# Initialise variables
active_sprites = pygame.sprite.Group()
active_sprites.add(player)

# dangers = Dangers(dangers_quantity, 10, bottom_colour)

end = False

while not end:
  
  # Check for events
  for event in pygame.event.get():
    if event.type == QUIT:
      end = True

  # Check for keypresses
    if event.type == KEYDOWN:
      if event.key == K_LEFT or event.key == K_a:
        player.move_x(-movement_speed)
      # dangers.move(2)
      
      if event.key == K_RIGHT or event.key == K_d:
        player.move_x(movement_speed)
      # dangers.move(-2)
      
      if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
        player.jump(jump_height)
    
    if event.type == KEYUP:
      if (event.key == K_LEFT or event.key == K_a) and player.speed_x < 0:
        player.stop()
      if (event.key == K_RIGHT or event.key == K_d) and player.speed_x > 0:
        player.stop()

    if event.type == MOUSEBUTTONUP:
      if event.button == 1:
        current_level.open_blue_portal(pygame.mouse.get_pos())
      if event.button == 3:
        current_level.open_orange_portal(pygame.mouse.get_pos())


  active_sprites.update()
  current_level.update()

  if player.rect.right >= start_right_shift:
    diff = start_right_shift - player.rect.right
    player.rect.right = start_right_shift
    current_level.shift_world(diff)

  if player.rect.left <= start_left_shift:
    diff = start_left_shift - player.rect.left
    player.rect.left = start_left_shift
    current_level.shift_world(diff)

  # Check for player still alive
  # if dangers.collision(player.rect):
    #print("Game lost!")
    #end = True

  # Goal reached
  #if world.on_goal(player.rect):
  #  print("Game won!")
  #  end = True
  
  # Render frame
  current_level.draw(screen)
  active_sprites.draw(screen)

  # Set the clock
  clock.tick(40)
  
  # Update display
  pygame.display.update()

pygame.display.quit()
sys.exit()
