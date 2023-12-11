import pygame
import os
import sys

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
        return image
    return image


class Cursor(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]
        if not pygame.mouse.get_focused():
            self.rect.x = -100
            self.rect.y = -100


all_sprites = pygame.sprite.Group()
Cursor(all_sprites)

if __name__ == '__main__':
    running = True
    moving = False
    while running:
        screen.fill((0, 0, 0))
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        all_sprites.update(event)
        pygame.display.flip()
    pygame.quit()
