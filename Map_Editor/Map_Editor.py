# Map editor
import pygame
import button_class
import sys
import os
import csv
from pygame.locals import *
from Map_editor_config import *


class Editor:

    def __init__(self):

        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN,SCREEN_HEIGHT + LOWER_MARGIN))
        self.title = pygame.display.set_caption("Map Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("8-bit.ttf" , 20)
        #self.font = pygame.font.SysFont("8-bit.ttf" , 50)

        self.img_folder = os.listdir("Tile sprites")
        self.bg_image = pygame.image.load("ME_BG_IMG3.png").convert()
        self.extensions = ('.png' , '.jpg')

        self.program_running = True

        self.zoom_in = 0
        self.zoom_out = 0
        self.scroll_vertical = 0
        self.scroll_horizontal = 0
        self.increase_speed = False

        self.btn_count = 0
        self.cur_count = 0
        self.current_tile = 0

        self.level = 0

    def main_loop(self):
        self.tile_loader()
        self.event()
        self.render_bg()
        self.render_world()
        self.sprite_grid()
        self.button_panel()
        self.tile_buttons()
        self.mouse_input()
        self.level_text(f'Level: {self.level}' , self.font , BLACK, 10 , 630)

    def level_text(self,text, font , color , x , y ):

        instructions = self.font.render("Press UP/DOWN arrow to change level" , False , GREY)
        text_render = self.font.render(text , False , GREY)
        self.screen.blit(text_render , (x,y))
        self.screen.blit(instructions , (10,610))

    def game_style_select(self):

        player_input = "Choose Game Style"
        print(player_input)

    def mapping_world_data(self):

        #creates default world maps!

        self.world_data = []

        for row in range(GRID_ROWS):
            gr = [-1] * (GRID_ROWS + 135)
            self.world_data.append(gr)

        for row in range(GRID_COLUMNS):
            gc = [-1] * (GRID_COLUMNS + 25)
            self.world_data.append(gc)


    def tile_loader(self):

        self.img_array = []

        self.save_btn = pygame.image.load("Save_button.png").convert()
        self.load_btn = pygame.image.load("Load_button.png").convert()

        for tiles in sorted(self.img_folder):
            ext = os.path.splitext(tiles)[-1].lower()
            if ext in self.extensions:
                self.img_tiles = pygame.image.load(os.path.join("Tile sprites",tiles)).convert()
                self.img_tiles = pygame.transform.scale(self.img_tiles , (TILE_SIZE , TILE_SIZE ))
                self.img_array.append(self.img_tiles)

    def button_panel(self):

        mouse_pos = pygame.mouse.get_pos()
        btn_scroll = 0

        self.scroll_panel = pygame.Surface((220 , 300))
        self.scroll_panel.fill(GREY)

        self.scroll_panel_rect = self.scroll_panel.get_rect(topleft = (SCREEN_WIDTH + 35 , 75))
        self.screen.blit(self.scroll_panel , self.scroll_panel_rect)

        self.btn_panel_collide = self.scroll_panel_rect.collidepoint(mouse_pos)

    def tile_buttons(self):

        self.btn_array = []

        self.btn_row = 0
        self.btn_col = 0

        mouse_pos = pygame.mouse.get_pos()

        for i in range(len(self.img_array)):
            self.btn_tile = button_class.Button(SCREEN_WIDTH + (75 * self.btn_col) + 50 , 75 * self.btn_row + 100 , self.img_array[i] , 1)
            self.btn_array.append(self.btn_tile)
            self.btn_col += 1
            if self.btn_col == 3:
                self.btn_row +=1
                self.btn_col = 0
                if len(self.btn_array) > len(self.img_array):
                    print("array limit reached")
                    break

        # calls Button class , gets method from class(render_button)
        for self.btn_count , i  in enumerate(self.btn_array):
            if i.render_button(self.screen):
                self.current_tile = self.btn_count
                #print(self.current_tile)

        pygame.draw.rect(self.screen , BLUE , self.btn_array[self.current_tile].rect, 3)

        save_button = button_class.Button(SCREEN_WIDTH + 10, SCREEN_HEIGHT + LOWER_MARGIN - 100, self.save_btn , .5)
        load_button = button_class.Button(SCREEN_WIDTH + 150 , SCREEN_HEIGHT + LOWER_MARGIN - 100, self.load_btn , .5)

        save_rect = save_button.render_button(self.screen)
        load_rect = load_button.render_button(self.screen)

        if save_rect and pygame.mouse.get_pressed()[0]:
            #takes level var and writes to file. delimiter ',' is to seperate values ( -1,0,1,2,etc) in csv file
            with open(f'level{self.level}_data.csv' , 'w' , newline='') as csvfile:
                write_level = csv.writer(csvfile, delimiter=',')
                for row in self.world_data:
                    write_level.writerow(row)

        if load_rect and pygame.mouse.get_pressed()[0]:
            self.scroll_vertical = 0
            self.scroll_horizontal = 0
            try:
                with open(f'level{self.level}_data.csv' , newline='') as csvfile:
                    read_level = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(read_level):
                        for y , tile in enumerate(row):
                            self.world_data[x][y] = int(tile)
            except:
                self.level_text("No such level" , self.font , BLACK, 10 ,650)


    def sprite_grid(self):

        #vertical lines
        for c in range(GRID_COLUMNS + 25):
            pygame.draw.line(self.screen, BLACK, (c * TILE_SIZE - self.scroll_vertical, 0) , (c * TILE_SIZE - self.scroll_vertical, SCREEN_HEIGHT))

        #horizontal lines
        for r in range(GRID_ROWS + 135):
            pygame.draw.line(self.screen, BLACK, (0, r * TILE_SIZE - self.scroll_horizontal) , (SCREEN_WIDTH, r * TILE_SIZE - self.scroll_horizontal))

        # creating side panel and rect!
        self.side_panel = pygame.Surface((SIDE_MARGIN,SCREEN_HEIGHT))
        self.side_panel.fill(BLACK)

        self.side_rect = self.side_panel.get_rect(topright = (SCREEN_WIDTH + SIDE_MARGIN,0))

        self.screen.blit(self.side_panel, self.side_rect)

        #creating bottom panel and rect
        self.bottom_panel = pygame.Surface((SCREEN_WIDTH * 1.5, LOWER_MARGIN))
        self.bottom_panel.fill(BLACK)

        self.bottom_rect = self.bottom_panel.get_rect(topleft = (0, SCREEN_HEIGHT))

        self.screen.blit(self.bottom_panel, self.bottom_rect)

    def render_world(self):

        for  y, row in enumerate(self.world_data):
            for x , tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(self.img_array[tile], ( x  * TILE_SIZE -self.scroll_vertical, y  * TILE_SIZE -self.scroll_horizontal))

    def render_bg(self):

        self.clock.tick(FPS)

        self.img_size = self.bg_image.get_size()
        self.screen.fill(GREY)

        for x in range(6):
            self.screen.blit(self.bg_image, ((x * self.img_size[1]) -self.scroll_vertical, -self.scroll_horizontal))
        for y in range(6):
            self.screen.blit(self.bg_image, ((y * self.img_size[1]) -self.scroll_vertical , self.bg_image.get_height() - self.scroll_horizontal))


    def mouse_input(self):

        can_click = True

        m_pos = pygame.mouse.get_pos()
        x = (m_pos[0] + self.scroll_vertical) // TILE_SIZE
        y = (m_pos[1] + self.scroll_horizontal) // TILE_SIZE

        b_collide = self.bottom_rect.collidepoint(m_pos)
        s_collide = self.side_rect.collidepoint(m_pos)

        if self.btn_panel_collide:
            pass

        if b_collide or s_collide:
            can_click = False
        else:
            can_click = True
            if can_click == True and pygame.mouse.get_pressed()[0] == 1:
                if self.world_data[y][x] != self.current_tile:
                    self.world_data[y][x] = self.current_tile

            if can_click == True and pygame.mouse.get_pressed()[2] == 1:
                self.world_data[y][x] = -1


    def event(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_PAGEUP]:
            pass

        #toggles  scrolling speed
        if keys[pygame.K_LSHIFT]:
            self.increase_speed = True
        else:
            self.increase_speed = False

        #scrolls up
        if keys[pygame.K_w] and self.scroll_horizontal > 0:
            self.scroll_horizontal -= 10
            if self.increase_speed and self.scroll_horizontal > 0:
                self.scroll_horizontal -= 20

        #scrolls down
        if keys[pygame.K_s] and self.scroll_horizontal < MAX_PIXEL_MAP_H:
            self.scroll_horizontal += 10
            if self.increase_speed:
                self.scroll_horizontal += 20

        #scrolls left
        if keys[pygame.K_a] and self.scroll_vertical > 0:
            self.scroll_vertical -= 10
            if self.increase_speed and self.scroll_vertical > 0:
                self.scroll_vertical -= 20

        #scrolls right
        if keys[pygame.K_d] and self.scroll_vertical < MAX_PIXEL_MAP_W:
            self.scroll_vertical += 10
            if self.increase_speed:
                self.scroll_vertical += 20


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.level += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self.level > 0:
                    self.level -= 1

        pygame.display.update()

def run_program():

    ME = Editor()
    ME.game_style_select()
    ME.mapping_world_data()

    while ME.program_running:
        ME.main_loop()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_program()
