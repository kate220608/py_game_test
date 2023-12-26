import pygame
import os
import sys

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


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


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, key):
        pos = self.pos
        if key == pygame.K_UP:
            self.pos = self.pos[0], self.pos[1] - 1
            self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                                   tile_height * self.pos[1] + 5)
        elif key == pygame.K_DOWN:
            self.pos = self.pos[0], self.pos[1] + 1
            self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                                   tile_height * self.pos[1] + 5)
        elif key == pygame.K_RIGHT:
            self.pos = self.pos[0] + 1, self.pos[1]
            self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                                   tile_height * self.pos[1] + 5)
        elif key == pygame.K_LEFT:
            self.pos = self.pos[0] - 1, self.pos[1]
            self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                                   tile_height * self.pos[1] + 5)
        if pygame.sprite.spritecollideany(self, tiles_group).tile_type == 'wall':
            self.pos = pos
            self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                                   tile_height * self.pos[1] + 5)


tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                level[y][x] = '.'
                new_player = Player(x, y)
    return new_player, x, y


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Правила игры",
                  "Игрок двигается",
                  "при нажатии кнопок"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.display.set_caption('Марио')
    start_screen()
    level_map = load_level(input())
    player, level_x, level_y = generate_level(level_map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                player.move(event.key)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
