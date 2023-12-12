import pygame
import os
import sys


pygame.init()
size = width, height = 600, 95
screen = pygame.display.set_mode(size)
v = 1
fps = 30
clock = pygame.time.Clock()


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


class Car(pygame.sprite.Sprite):
    image = load_image("car2.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = 0
        self.right_moving = True

    def update(self):
        if self.right_moving:
            self.rect = self.rect.move(self.x, 0)
            self.x += v / fps
        else:
            self.rect = self.rect.move(-self.x, 0)
            self.x -= v / fps
        clock.tick(fps)
        if self.rect.x + 150 >= 600:
            self.right_moving = False
        if self.rect.x <= 0:
            self.right_moving = True


all_sprites = pygame.sprite.Group()
Car(all_sprites)

if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
    pygame.quit()