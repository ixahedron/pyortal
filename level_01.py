from configuration import *

# every platform: width, height, x, y
level = [
         [20, screen_y, -300, 0],
         [1900, 20, -300, 0],
         [1900, 20, -300, screen_y - 20],
         [1210, 10, 50, 500],
         [10, 130, 700, 400],
         [1210, 10, 50, 280],
         [10, 310, 1400, 180],
         [exit_width + 20, int(0.3 * screen_y), 1580, 0],
         [exit_width + 20, int(0.7 * screen_y - exit_height), 1580, int(0.3 * screen_y + exit_height)]
         ]

left_border = level[0][2]
top_border = -50
bottom_border = screen_y

cubes = [(60, 450),
         (100, 510)]

buttons = [
           (100, 500),
   #        (500, 280)
           ]
doors = [
         (200, 500),
    #     (1570, 0.50 * screen_y)            
        ]

exit_x = 1600
exit_y = 0.3 * screen_y 

