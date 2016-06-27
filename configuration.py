use_menu = True
text_size_menu = 32
logo_menu = "res/logo_resized.png"

mp_host = '127.0.0.1'
mp_port1 = 10103
mp_port2 = 10104

game_title = 'Portal 2d wannabe'

screen_x = 800
screen_y = 600
player_start_x = 50
player_start_y = 200
window_size = (screen_x, screen_y)

start_right_shift = screen_x * 0.7
start_left_shift = screen_x * 0.3

platform_colour = (205, 133, 63)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

gravity = 0.35
jump_height = -8.5
maximum_vertical_velocity = 50
movement_speed = 5
friction = 0.2

player_image = "res/ninjacat_2_fix.png"
player_width = 40
player_height = 60

bg_image_default = "res/back.png"
bg_image_01 = "res/back_03.jpg"

platform_image = "res/platform_1.jpg"

cube_image = "res/cube_image.png"
cube_edge = 30

button_image = "res/button.png"
button_w = 40
button_h = 15

door_image = "res/platform_1.png"
door_w = 10
door_h = 160

portal_blue_image = "res/portal_blue.png"
portal_orange_image = "res/portal_orange.png"
portal_width = 80
portal_height = 80

exit_image = "res/exit_image.png"
exit_width = 70
exit_height = 70

# Directions
UP = (0, -player_height - 3)
DOWN = (0, 0.5 * player_height + 3)
RIGHT = (0.5 * player_width + 3, 0)
LEFT = (-3 - player_width, 0)
