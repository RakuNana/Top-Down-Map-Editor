import pygame
import time
import math
import random
from config import *
from pygame.locals import *


class Sprite_sheets:

    def __init__(self,file):

        self.sheet = pygame.image.load(file).convert()

    def grab_sprite(self,x,y,width,height):

        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)

        return sprite

class Player(pygame.sprite.Sprite):

    def __init__(self,game,x,y):

        self.game = game
        self._layer = PLAYER_LAYER

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.player_sheet.grab_sprite(0,0,self.width,self.height)

        self.facing = "down"

        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.walk_loop = 0


    def update(self):

        self.movement()
        self.walk_animations()

        self.rect.y += self.y_change

        self.rect.x += self.x_change

        self.y_change = 0
        self.x_change = 0


    def movement(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"

        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"

        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"

        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"

        if keys[pygame.K_d] and keys[pygame.K_a]:
            self.y_change = 0

    def detect_collision(self):
        pass

    def walk_animations(self):

        walk_down = [self.game.player_sheet.grab_sprite(18,1,self.width,self.height),
                self.game.player_sheet.grab_sprite(35,1,self.width,self.height)       ]

        walk_up = [self.game.player_sheet.grab_sprite(18,18,self.width,self.height),
                    self.game.player_sheet.grab_sprite(35,18,self.width,self.height)]

        walk_left = [self.game.player_sheet.grab_sprite(52,1,self.width,self.height),
                    self.game.player_sheet.grab_sprite(69,1,self.width,self.height)]

        walk_right = [self.game.player_sheet.grab_sprite(52,18,self.width,self.height),
                        self.game.player_sheet.grab_sprite(69,18,self.width,self.height)]


        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.player_sheet.grab_sprite(18,1,self.width,self.height)
            else:
                self.image = walk_down[math.floor(self.walk_loop)]
                self.walk_loop += 0.1
                if self.walk_loop >= 2:
                    self.walk_loop = 0

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.player_sheet.grab_sprite(18,18,self.width,self.height)
            else:
                self.image = walk_up[math.floor(self.walk_loop)]
                self.walk_loop += 0.1
                if self.walk_loop >= 2:
                    self.walk_loop = 0

        if self.facing == "left":
            if self.x_change == 0 :
                self.image = self.game.player_sheet.grab_sprite(52,1,self.width,self.height)
            else:
                self.image = walk_left[math.floor(self.walk_loop)]
                self.walk_loop += 0.1
                if self.walk_loop >= 2:
                    self.walk_loop = 0

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.player_sheet.grab_sprite(52,18,self.width,self.height)
            else:
                self.image = walk_right[math.floor(self.walk_loop)]
                self.walk_loop += 0.1
                if self.walk_loop >= 2:
                    self.walk_loop = 0
