import pygame
from pygame.locals import RLEACCEL
from PIL import Image
from random import shuffle, randint


class Tile(pygame.sprite.Sprite):

    def __init__(self, cropped_image):
        pygame.sprite.Sprite.__init__(self)
        self.cropped_image = cropped_image
        self.image = pygame.image.fromstring(self.cropped_image.tobytes(), self.cropped_image.size, self.cropped_image.mode)
        self.image.set_alpha(128)
        self.image.convert()
        #self.image.set_alpha(128)
        #self.image.set_colorkey(-1, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.over = False

    def hidden(self):
        self.image.fill((255, 255, 255))

    def click(self, mouse):
        if self.rect.collidepoint(mouse):
            print("hit RED")
            self.image.fill(pygame.Color(0, 0, 0, 0))
            self.image.set_alpha(128)
            #self.image.set_alpha(128)
            #self.image.fill((255, 255, 255, 1), None, pygame.BLEND_RGBA_MULT)
            #self.image.fill(pygame.Color(40, 50, 50, 128), None, pygame.BLEND_RGBA_MULT)

    def mouse_out(self):
        self.over = False
        self.image = pygame.image.fromstring(self.cropped_image.tobytes(), self.cropped_image.size,
                                             self.cropped_image.mode)

    def mouse_over(self, mouse):
        if not self.over:
            if self.rect.collidepoint(mouse):
                #self.image.fill((255, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)
                self.image.fill(pygame.Color(40, 50, 50, 128), None, pygame.BLEND_RGBA_MULT)
                self.over = True


def main():
    pygame.init()
    #display = pygame.display.set_mode((image_obj.width, image_obj.height))
    display = pygame.display.set_mode((960, 641))
    display.fill(0xFFFFFF)
    pygame.display.set_caption('Slide Puzzle')

    all_sprites_list = pygame.sprite.Group()
    image_obj = Image.open('assets/image.jpg')
    tiles = []
    tile_row_count = 5
    tile_col_count = 5
    tile_width = image_obj.width / tile_col_count
    tile_height = image_obj.height / tile_row_count
    positions = []
    for x in range(tile_row_count):
        row = []
        for y in range(tile_col_count):
            # left, upper, right, lower
            left = x * tile_width
            upper = y * tile_height
            right = left + tile_width
            lower = upper + tile_height
            cropped_image = image_obj.crop((left, upper, right, lower))
            #row.append(pygame.image.fromstring(cropped_image.tobytes(), cropped_image.size, cropped_image.mode))
            t = Tile(cropped_image)
            #row.append(t)
            all_sprites_list.add(t)
            positions.append((x * tile_width, y * tile_height))
        tiles.append(row)

    # randomize tiles
    shuffle(positions)
    # choose one to be the blank space
    blank_index = randint(0, len(positions))

    for i, sprite in enumerate(all_sprites_list.sprites()):
        pos = positions[i]
        sprite.rect.x = pos[0]
        sprite.rect.y = pos[1]
        if i == blank_index:
            sprite.hidden()

    is_running = True
    clock = pygame.time.Clock()
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            # elif event.type == pygame.MOUSEMOTION:
            #     for s in all_sprites_list:
            #         s.mouse_out()
            #         if s.is_mouse_over(event.pos):
            #             s.mouse_over()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for s in all_sprites_list:
                    s.click(event.pos)

        for s in all_sprites_list:
            s.mouse_out()
            s.mouse_over(pygame.mouse.get_pos())

        all_sprites_list.update()
        all_sprites_list.draw(display)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
