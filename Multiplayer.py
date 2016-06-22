import pygame
import sys
from pygame.locals import *
import socket

from configuration import *
from Player import *
from Level import *

# Initialise mixer

# Init server
def init_server():
  
  # Create a TCP socket.
  ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
  # Flush on every send.
  ss.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
  ss.settimeout(15)
  
  # We will accept connections from all IPs on port 10101
  p = int(input())
  ss.bind(('0.0.0.0', p))
  # We will accept all connections with zero backlog.
  ss.listen(0)
  
  # This blocks until we accept a client connection, `cs` is the client socket.
  # Probably needs a separate thread?
  cs, client_addr = ss.accept()
  # Not block on read if nothing has been sent by the client, fail with exception.
  cs.setblocking(False)

  return (ss, cs)

# Init client
def init_client():
  
  # Create a TCP socket.
  cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
  # Flush on every send.
  cs.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
  
  p = int(input())
  # Connect to the server on the specified host and port.
  cs.connect((mp_host, p))
  # Not block on read if nothing has been sent by the server, fail with exception.
  cs.setblocking(False)

  return cs

def init_network():
  
  # Send smth. to the server.
  cs.send('c')
  # Try reading a char from the server, continue if nothing sent.
  try:
    cs.recv(1)
  except socket.error:
    pass
  # Kill the server connection.
  cs.shutdown(socket.SHUT_RDWR)
  

def main():
  screen = pygame.display.get_surface()
  clock = pygame.time.Clock()
  
  order = int(input())

  if order == 1:
    (ss, scs) = init_server()
    cs = init_client()
  else:
    cs = init_client()
    (ss, scs) = init_server()

  #Initialise player
  player = Player()
  player.rect.x = player_start_x + (order % 2) * 100
  player.rect.y = player_start_y
  
  player2 = Player()
  player2.rect.x = player_start_x + ((order + 1) % 2) * 100
  player2.rect.y = player_start_y


  # Initialise levels
  levels = []
  levels.append(Level_01(player, player2))
  
  current_level_number = 0 # start_with_level_number
  current_level = levels[current_level_number]
  
  player.level = current_level
  player2.level = current_level
  
  # Initialise variables
  active_sprites = pygame.sprite.Group()
  active_sprites.add(player)
  active_sprites.add(player2)
  
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
    if player.on_goal() and player2.on_goal():
      if current_level_number < len(levels)-1:
        player.rect.x = start_left_shift + (order % 2) * 100
        player2.rect.x = start_left_shift + ((order + 1) % 2) * 100
        current_level_number += 1
        current_level = levels[current_level_number]
        player.level = current_level
        player2.level = current_level
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

  # Kill the client socket.
  cs.shutdown(socket.SHUT_RDWR)
  
  # Kill the client connection.
  scs.shutdown(socket.SHUT_RDWR)
  
  # Kill the server socket.
  ss.shutdown(socket.SHUT_RDWR)
  
