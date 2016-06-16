import pygame
import sys
from pygame.locals import *

from configuration import *
from Player import *
from Level import *
from Menu import *

# Initialise mixer

# Initialise pygame
def initialise():
  pygame.init()

  window = pygame.display.set_mode(window_size)

  pygame.display.set_caption(game_title)

def menu():
  screen = pygame.display.get_surface()
  menu = Menu(("Start", "Exit"))
  menu.draw(screen)
  return menu.controls()

def main(start_with_level_number):
  screen = pygame.display.get_surface()
  clock = pygame.time.Clock()

  #Initialise player
  player = Player()
  player.rect.x = player_start_x
  player.rect.y = player_start_y
  
  # Initialise levels
  levels = []
  levels.append(Level_01(player))
  
  current_level_number = start_with_level_number
  current_level = levels[current_level_number]
  
  player.level = current_level
  
  # Initialise variables
  active_sprites = pygame.sprite.Group()
  active_sprites.add(player)
  
  end = False
  
  while not end:
    
    # Check for events
    for event in pygame.event.get():
      if event.type == QUIT:
        end = True
  
    # Check for keypresses
      if event.type == KEYDOWN:
        if event.key == K_LEFT or event.key == K_a:
          player.movement_key_pressed = True
          player.set_in_motion(-movement_speed)
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = True
            player.holded_object.set_in_motion(-movement_speed)
        
        if event.key == K_RIGHT or event.key == K_d:
          player.movement_key_pressed = True
          player.set_in_motion(movement_speed)
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = True
            player.holded_object.set_in_motion(movement_speed)
        
        if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
          player.jump(jump_height)
      
        if event.key == K_ESCAPE or event.key == K_q:
          end = True
        
        if (event.key == K_f):
          player.try_pickup() if player.hands_empty else player.drop_holded()
              
      if event.type == KEYUP:

        if (event.key == K_LEFT or event.key == K_a) and player.speed_x < 0:
          player.movement_key_pressed = False
          player.stop()
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = False
            player.holded_object.stop()

        if (event.key == K_RIGHT or event.key == K_d) and player.speed_x > 0:
          player.movement_key_pressed = False
          player.stop()
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = False
            player.holded_object.stop()

        if (event.key == K_s):
          print(player.movement_key_pressed)
  
      if event.type == MOUSEBUTTONUP:
        if event.button == 1:
          current_level.open_portal(pygame.mouse.get_pos(), True)
        if event.button == 3:
          current_level.open_portal(pygame.mouse.get_pos(), False)
  
  
    active_sprites.update()
    current_level.update()
  
    object_start_shift = player if player.hands_empty else player.holded_object
    if object_start_shift.rect.right >= start_right_shift and current_level.exit.sprite.rect.x > screen_x - exit_width : # so that the world doesn't shift if exit is in sight
      diff = start_right_shift - object_start_shift.rect.right
      object_start_shift.rect.right = start_right_shift
      if not player.hands_empty:
        player.rect.right = start_right_shift - player.holded_object.rect.width - player.rect.width / 4
      current_level.shift_world(diff)
  
    if object_start_shift.rect.left <= start_left_shift and current_level.world_shift < -current_level.left_border:
      diff = start_left_shift - object_start_shift.rect.left
      object_start_shift.rect.left = start_left_shift
      if not player.hands_empty:
        player.rect.left = start_left_shift + player.holded_object.rect.width + player.rect.width / 4
      current_level.shift_world(diff)
         
    
    # Check for player still alive
    # if dangers.collision(player.rect):
      #print("Game lost!")
      #end = True
  
    # Goal reached
    if player.on_goal():
      if current_level_number < len(levels)-1:
        player.rect.x = start_left_shift
        current_level_number += 1
        current_level = levels[current_level_number]
        player.level = current_level
      else:
        print("Game won!")
        end = True
    
    # Render frame
    current_level.draw(screen)
    active_sprites.draw(screen)
  
    # Set the clock
    clock.tick(40)
    
    # Update display
    pygame.display.update()
  

if __name__ == "__main__":
  initialise()
  if use_menu:
    level_no = menu()
    main(level_no)
  else:
    main(0)
  pygame.display.quit()
  sys.exit()
