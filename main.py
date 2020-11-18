import pygame

WIDTH = 600
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
done = False

pygame.display.set_caption('Tetris')
icon = pygame.image.load(r'pictures/icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load(r'pictures/background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()

pygame.mixer.music.load(r'music/gameBackground.mp3')
pygame.mixer.music.play(-1)

left_feld = 25
right_feld = 25

blocks_img = list()
for i in range(7):
    block_img = pygame.image.load(f'pictures/block_{i}.png').convert()
    blocks_img.append(block_img)

class gray_block(pygame.sprite.Sprite):
    def __init__(self, x, y, back):
        pygame.sprite.Sprite.__init__(self)
        if back == False:
            self.image = pygame.transform.scale(blocks_img[0], (25, 25))
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.top = y
        else:
            self.image = pygame.Surface((250, 500))
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.left = left_feld + 25
            self.rect.top = right_feld + 25

    def update(self):
        pass

for i in range(12):
    for j in range(22):
        if i == 0 or i == 11 or j == 0 or j == 21:
            block = gray_block(left_feld + i * 25, right_feld + j * 25, False)
            all_sprites.add(block)
block = gray_block(0, 0, True)
all_sprites.add(block)

while not done:
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # update

        # draw

        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        pygame.display.flip()
        # to do
        # pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 90, 90))
        #  pygame.display.flip()
