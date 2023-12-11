import pygame
import os
import sys

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Creature(pygame.sprite.Sprite):
    image = load_image("creature.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Creature.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 10
            elif keys[pygame.K_RIGHT]:
                self.rect.x += 10
            elif keys[pygame.K_UP]:
                self.rect.y -= 10
            elif keys[pygame.K_DOWN]:
                self.rect.y += 10


all_sprites = pygame.sprite.Group()
Creature(all_sprites)

if __name__ == '__main__':
    running = True
    while running:
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
        pygame.display.flip()
    pygame.quit()
