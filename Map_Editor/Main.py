import pygame
import sys
import time
from pygame.locals import *
from Player import *
from config import *


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((WIN_H,WIN_W) , pygame.RESIZABLE)
        self.title = pygame.display.set_caption("A Mothers Sun")
        self.menu_bar_icon = pygame.image.load("/home/raku/Documents/Pygame Games/A Mothers Sun/Game Sprites/Window_icon.png").convert()
        self.set_icon = pygame.display.set_icon(self.menu_bar_icon)
        self.clock = pygame.time.Clock()
        self.program_running = True

        self.player_sheet = Sprite_sheets("Game Sprites/OverWorld Sprites/Oscuro_OW/OSCURO_SHEET.png")


    def tile_mapper(self):
        pass


    def set_up(self):

        self.playing_game = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.npc= pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()

        self.player = Player(self,1,2)

    def update(self):

        self.all_sprites.update()

    def render(self):

        self.screen.fill(GRAY)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing_game = False
                self.program_running = False

    def main(self):

        while self.playing_game:
            self.events()
            self.update()
            self.render()

        self.program_running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

def run_program():

    G = Game()
    G.set_up()

    while G.program_running:
        G.main()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_program()
