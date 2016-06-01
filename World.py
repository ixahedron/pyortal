import pygame

class World():
  def __init__(self, level, block_size, block_colour, goal_colour):
        self.blocks = []
        self.goals = []
        self.posn_y = 0
        self.block_colour = block_colour
        self.goal_colour = goal_colour
        self.block_size = block_size

        for line in level:
              self.posn_x = 0
              for block in line:
                    if block == "-":
                          self.blocks.append(pygame.Rect(self.posn_x, self.posn_y, block_size, block_size))
                    if block == "Z":
                          self.goals.append(pygame.Rect(self.posn_x, self.posn_y, block_size, block_size))
                    self.posn_x = self.posn_x + block_size
              self.posn_y = self.posn_y + block_size
              

  def move(self, width):
        for block in self.blocks + self.goals:
            block.move_ip(width, 0)
 
  def touch_x(self, player_rect):
    return_x = -1
    for block in self.blocks:
      if block.colliderect(player_rect):
        return_x = block.x
    return return_x

  def touch_y(self, player_rect):
        return_y = -1
        for block in self.blocks:
              if block.colliderect(player_rect):
                    return_y = block.y - block.height + 1
        return return_y
 
  def on_goal(self, player_rect):
        for block in self.goals:
              if block.colliderect(player_rect):
                  return True
        return False
 
  def update(self, screen):
        for block in self.blocks:
              pygame.draw.rect(screen, self.block_colour, block, 0)
        for block in self.goals:
              pygame.draw.rect(screen, self.goal_colour, block, 0)
