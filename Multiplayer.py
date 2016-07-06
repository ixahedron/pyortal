import pygame
import sys
from pygame.locals import *
import socket

from configuration import *
from Player import *
from Level import *

# Initialise mixer
try:
    input = raw_input
except NameError:
    pass

# Init server
def init_server(port = None):
  
  # Create a TCP socket.
  ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
  # Flush on every send.
  ss.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
  ss.settimeout(20)
  
  # We will accept connections from all IPs on port 10101
  port = port if port is not None else int(input())
  ss.bind(('0.0.0.0', port))
  # We will accept all connections with zero backlog.
  ss.listen(0)
  
  # This blocks until we accept a client connection, `cs` is the client socket.
  # Probably needs a separate thread?
  cs, client_addr = ss.accept()
  # Not block on read if nothing has been sent by the client, fail with exception.
  cs.setblocking(False)

  return (ss, client_addr[0], cs)

# Init client
def init_client(host, port = None):
  
  # Create a TCP socket.
  cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
  # Flush on every send.
  cs.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
  
  port = port if port is not None else 31337
  host = host if len(host) > 0 else mp_host
  # Connect to the server on the specified host and port.
  cs.connect((host, port))
  # Not block on read if nothing has been sent by the server, fail with exception.
  cs.setblocking(False)

  return cs


def main(order, host = None):
  screen = pygame.display.get_surface()
  clock = pygame.time.Clock()
  
  if order % 2 == 1:
    (ss, sca, scs) = init_server(mp_port1)
    cs = init_client(sca, mp_port2)
  else:
    cs = init_client(host, mp_port1)
    (ss, sca, scs) = init_server(mp_port2)

  #Initialise player
  player = Player(order % 2)
  player.rect.x = player_start_x + (order % 2) * 100
  player.rect.y = player_start_y
  
  player2 = Player((order+1) % 2)
  player2.rect.x = player_start_x + ((order + 1) % 2) * 100
  player2.rect.y = player_start_y

  # Initialise levels
  levels = []
  levels.append(Level_M_01(player, player2))
  
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
        cs.send(b'q')
        end = True
  
    # Check for keypresses
      if event.type == KEYDOWN:
        if event.key == K_LEFT or event.key == K_a:
          cs.send(b'a')
          player.movement_key_pressed = True
          player.set_in_motion(-movement_speed)
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = True
            player.holded_object.set_in_motion(-movement_speed)
        
        if event.key == K_RIGHT or event.key == K_d:
          cs.send(b'd')
          player.movement_key_pressed = True
          player.set_in_motion(movement_speed)
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = True
            player.holded_object.set_in_motion(movement_speed)
        
        if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
          cs.send(b'w')
          player.jump(jump_height)
      
        if event.key == K_ESCAPE or event.key == K_q:
          cs.send(b'q')
          end = True
        
        if (event.key == K_f):
          cs.send(b'f')
          player.try_pickup() if player.hands_empty else player.drop_holded()
              
      if event.type == KEYUP:

        if (((event.key == K_LEFT or event.key == K_a) and player.speed_x < 0) or
            ((event.key == K_RIGHT or event.key == K_d) and player.speed_x > 0)):
          cs.send(b'u')
          player.movement_key_pressed = False
          player.stop()
          if not player.hands_empty:
            player.holded_object.movement_key_pressed = False
            player.holded_object.stop()

        if (event.key == K_s):
          print(player.movement_key_pressed)
  
      if event.type == MOUSEBUTTONUP:
        if event.button == 1:
          (x, y) = pygame.mouse.get_pos()
          
          bdx = str(x - player.rect.x).zfill(4).encode('utf-8')
          bdy = str(y - player.rect.y).zfill(4).encode('utf-8')

          cs.send(b'p')
          cs.send(bdx)
          cs.send(bdy)
          
          current_level.open_portal((x, y), order % 2 == 1)
  
    try_receiving = True
    commands = []
    while try_receiving:
      # Try reading a char from the server, continue if nothing sent.
      try:
        received = scs.recv(1).decode('utf-8')
        if received == "q":
          try_receiving = False
          end = True
          continue
        if received == "p":
          try:
            dx = int(scs.recv(4))
            dy = int(scs.recv(4))
            current_level.open_portal((player2.rect.x + dx, player2.rect.y + dy), order % 2 == 0, True)
          except:
            continue

        commands.append(received)
      except socket.error:
        try_receiving = False

    for comm in commands:
      if comm == "a":
        player2.movement_key_pressed = True
        player2.set_in_motion(-movement_speed)
        if not player2.hands_empty:
          player2.holded_object.movement_key_pressed = True
          player2.holded_object.set_in_motion(-movement_speed)
      elif comm == "d":
        player2.movement_key_pressed = True
        player2.set_in_motion(movement_speed)
        if not player2.hands_empty:
          player2.holded_object.movement_key_pressed = True
          player2.holded_object.set_in_motion(movement_speed)
      elif comm == "u":
        player2.movement_key_pressed = False
        player2.stop()
        if not player2.hands_empty:
          player2.holded_object.movement_key_pressed = False
          player2.holded_object.stop()
      elif comm == "w":
        player2.jump(jump_height)
      elif comm == "f":
        player2.try_pickup() if player2.hands_empty else player2.drop_holded()
      elif comm == "q":
        end = True
  
    active_sprites.update()
    current_level.update()
  
    object_start_shift = player if player.hands_empty else player.holded_object
    if object_start_shift.rect.right >= start_right_shift and current_level.exit.sprite.rect.right > screen_x : # so that the world doesn't shift if exit is in sight
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

  cs.send(b'q')

  # Kill the client socket.
  try:
    cs.shutdown(socket.SHUT_RDWR)
  except:
    pass
  
  # Kill the client connection.
  scs.shutdown(socket.SHUT_RDWR)
  
  # Kill the server socket.
  ss.shutdown(socket.SHUT_RDWR)
  
