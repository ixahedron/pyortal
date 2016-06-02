import pygame

game_title = 'Portal 2d wannabe'

screen_x = 800
screen_y = 600
player_start_x = 50
player_start_y = 200
window_size = (screen_x, screen_y)

start_right_shift = screen_x * 0.8
start_left_shift = screen_x * 0.2

block_colour = pygame.Color(205, 133, 63)
platform_colour = (205, 133, 63)
goal_colour = pygame.Color(255, 255, 0)
bottom_colour = pygame.Color(255, 0, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

gravity = 1
jump_height = -10
movement_speed = 5

player_image = "res/ninjacat_2_fix.png"
player_width = 40
player_height = 60

bg_image_default = "res/back.png"
bg_image_01 = "res/back_03.jpg"

platform_image = "res/platform_1.jpg"

portal_blue_image = "res/portal_blue.png"
portal_orange_image = "res/portal_orange.png"
portal_width = 70
portal_height = 80

# Directions
UP = 1
DOWN = -1
RIGHT = 2
LEFT = -2
