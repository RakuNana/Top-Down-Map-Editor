# Button class
import pygame

class Button:

    def __init__(self , x, y, image , scale):

        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale) , int(self.height * scale)))
        self.rect  = self.image.get_rect()
        self.rect.topleft = (x ,y)
        self.clicked = False

    def render_button(self, surface):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return self.clicked
