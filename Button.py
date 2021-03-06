from configuration import *
import pygame

class Button(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()

    self.level = None

    self.portal_supporting = False
    self.pressed = False

    self.door = None

  def update(self):
    self.rect.y -= 12
    player_collision = pygame.sprite.collide_rect(self, self.level.player)
    player2_collision = False
    if self.level.player2 is not None:
      player2_collision = pygame.sprite.collide_rect(self, self.level.player2)
    cube_collisions = pygame.sprite.spritecollideany(self, self.level.cubes)
    self.rect.y += 12

    if player_collision or player2_collision or cube_collisions:
      if not self.pressed:
        self.press()
    else:
      if self.pressed:
        self.unpress()

  def press(self):
    self.pressed = True
    button_pressed =  "res/Button_Press.wav"

    x = self.rect.x
    b = self.rect.bottom
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, int(0.5 * button_h)))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.bottom = b
    btn_snd = pygame.mixer.Sound(button_pressed)
    btn_snd.play()

    self.door.open()
    
  def unpress(self):
    self.pressed = False
    
    x = self.rect.x
    b = self.rect.bottom
    self.image = pygame.transform.scale(pygame.image.load(button_image), (button_w, button_h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.bottom = b

    self.door.close()
