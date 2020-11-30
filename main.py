import pygame
import numpy as np
import random

WIDTH = 600
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAX_COLORS = 7

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

def def_feld():
    for i in range(12):
        for j in range(22):
            if i == 0 or i == 11 or j == 0 or j == 21:
                block = gray_block(left_feld + i * 25, right_feld + j * 25, False)
                all_sprites.add(block)
    block = gray_block(0, 0, True)
    all_sprites.add(block)
    feld = np.array([[0] * 14] * 24)
    feld[1,] = 2
    feld[22,] = 2
    feld[:, 1] = 2
    feld[:, 12] = 2
    return feld

figures_base_dict = {
    'i' : {'form':np.array([[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]),'spawn':1, 'shape':4},
    'j' : {'form':np.array([[0,1,0],[0,1,0],[1,1,0]]),'spawn':1, 'shape':3},
    'l' : {'form':np.array([[0,1,0],[0,1,0],[0,1,1]]),'spawn':1, 'shape':3},
    't' : {'form':np.array([[0,1,0],[1,1,1],[0,0,0]]),'spawn':1, 'shape':3},
    's' : {'form':np.array([[0,0,0],[0,1,1],[1,1,0]]),'spawn':0, 'shape':3},
    'z' : {'form':np.array([[0,0,0],[1,1,0],[0,1,1]]),'spawn':0, 'shape':3},
    'o' : {'form':np.array([[1,1],[1,1]]),'spawn':1, 'shape':2},
}

def create_figure(figure_type):
    color = random.randint(1,MAX_COLORS)
    base = figures_base_dict[figure_type]
    for i in range(base['shape']):
        for j in range(base['shape']):
            if base['form'][i, j] == 1:
                block = action_block(SPAWN_x+j, base['spawn']+i,
                                     SPAWN_x+(base['shape']-1)/2,
                                     base['spawn']+(base['shape']-1)/2,
                                     color)
                all_sprites.add(block)
                figure_sprites.add(block)
    return {'x':SPAWN_x+2, 'y':base['spawn']+1, 'base':base['form'], 'shape':base['shape']}

class action_block(pygame.sprite.Sprite):
    def __init__(self, x, y, center_x, center_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = blocks_img[color]
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.centerx = x * 25 + 62
        self.rect.centery = y * 25 + 37
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
    def update(self):
        if action == 'left':
            self.x -= 1
            self.center_x -= 1
            self.rect.centerx -= 25
        if action == 'right':
            self.x += 1
            self.center_x += 1
            self.rect.centerx += 25
        if down_flag and action != 'down_const':
            self.y += 1
            self.center_y += 1
            self.rect.centery += 25
        if action == 'down_const':
            self.const()
        # if action == 'rotation_r':
        #     self.x, self.y = self.center_x + (self.y - self.center_y), self.center_y - (self.x - self.center_x)
        #     self.rect.centerx = 25 * (self.x) + 50
        #     self.rect.centery = 25 * (self.y) + 25
        # if action == 'rotation_l':
        #     self.x, self.y = self.center_x - (self.y - self.center_y), self.center_y + (self.x - self.center_x)
        #     self.rect.centerx = 25 * (self.x) + 50
        #     self.rect.centery = 25 * (self.y) + 25
    def const(self):
        block = position_block(self.x + 1, self.y, self.color)
        all_sprites.add(block)
        self.kill()

SPAWN_x = 4
def create_figure(figure_type):
    color = random.randint(1,MAX_COLORS-1)
    base = figures_base_dict[figure_type]
    for i in range(base['shape']):
        for j in range(base['shape']):
            if base['form'][i, j] == 1:
                block = action_block(SPAWN_x+j, base['spawn']+i,
                                     SPAWN_x+(base['shape']-1)/2,
                                     base['spawn']+(base['shape']-1)/2,
                                     color)
                all_sprites.add(block)
                figure_sprites.add(block)
    return {'x':SPAWN_x+2, 'y':base['spawn']+1, 'base':base['form'], 'shape':base['shape']}

class position_block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = blocks_img[color]
        self.rect = self.image.get_rect()
        self.rect.centerx = x * 25 + 37
        self.rect.centery = y * 25 + 37
        self.x = x
        self.y = y
    def update(self):
        if action == 'down_const':
            if win_vector[int(self.y) - 1] == 1:
                self.kill()
            else:
                down_vector = win_vector[::-1].cumsum()[::-1]
                self.y += down_vector[int(self.y) - 1]
                self.rect.centery = 25 * (self.y) + 37

def check_imposition(feld, figere_base, figure_x, figure_y, figure_shape):
    feld_loc = feld[figure_y:figure_y+figure_shape,figure_x:figure_x+figure_shape]
    if feld_loc.shape == figere_base.shape:
        return (feld_loc * figere_base).sum() > 0
    else:
        return True

def check_imposition(feld, figere_base, figure_x, figure_y, figure_shape):
    feld_loc = feld[figure_y:figure_y+figure_shape,figure_x:figure_x+figure_shape]
    if feld_loc.shape == figere_base.shape:
        return (feld_loc * figere_base).sum() > 0
    else:
        return True

def check_move(feld, active_figure, vector):
    return not check_imposition(feld, active_figure['base'],
                            active_figure['x']+vector[0],
                            active_figure['y']+vector[1],
                            active_figure['shape'])

def check_rotation(feld, active_figure, direction):
    if direction == 'r':
        new_base_figure = active_figure['base'].T[:,::-1]
        return not check_imposition(feld, new_base_figure,
                                active_figure['x'],
                                active_figure['y'],
                                active_figure['shape'])
    else:
        new_base_figure = active_figure['base'].T[::-1,:]
        return not check_imposition(feld, new_base_figure,
                                active_figure['x'],
                                active_figure['y'],
                                active_figure['shape'])

def update_feld(feld, fig):
    feld[fig['y']:fig['y']+fig['shape'],fig['x']:fig['x']+fig['shape']] += fig['base']
    return feld

def refresh_feld(feld):
    sub_feld = feld[2:-2,2:-2]
    for i in range(sub_feld.shape[0]):
        if win_vector[i] == 1:
            for j in range(i):
                sub_feld[i-j] = sub_feld[i-j-1]
            sub_feld[0] = 0
    feld[2:-2,2:-2] = sub_feld
    return feld

all_sprites = pygame.sprite.Group()
figure_sprites = pygame.sprite.Group()

feld = def_feld()

active_figure = create_figure('i')

step = 1
# while not done:
#         down_flag = False
#         # input
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
#         keystate = pygame.key.get_pressed()
#
#         action = ''
#         if keystate[pygame.K_DOWN] or step >= 100:
#             if check_move(feld, active_figure, [0, +1]):
#                 down_flag = True
#                 active_figure['y'] += 1
#                 step = 1
#             else:
#                 action = 'down_const'
#                 feld = update_feld(feld, active_figure)
#                 win_vector = (feld[2:-2, 2:-2].sum(axis=1) == 10) * 1
#                 feld = refresh_feld(feld)
#                 figure_sprites.update()
#                 step = 1
#             down = True
#         if action == 'down_const':
#             active_figure = create_figure(random.choice(list(figures_base_dict.keys())))
#             if check_imposition(feld, active_figure['base'], active_figure['x'], active_figure['y'],
#                                 active_figure['shape']):
#                 running = False
#         # update
#         all_sprites.update()
#
#         # draw
#         screen.blit(background, background_rect)
#         all_sprites.draw(screen)
#         pygame.display.flip()
#         # to do
#         # pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 90, 90))
#         #  pygame.display.flip()
#         step+=1

while not done:

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            done = True

    clock.tick(FPS)
    # Update
    # all_sprites.update()
    keystate = pygame.key.get_pressed()

    action = ''
    down_flag = False
    if keystate[pygame.K_DOWN] or step >= 10:
        if check_move(feld, active_figure, [0, +1]):
            down_flag = True
            active_figure['y'] += 1
            step = 1
        else:
            action = 'down_const'
            feld = update_feld(feld, active_figure)
            win_vector = (feld[2:-2, 2:-2].sum(axis=1) == 10) * 1
            feld = refresh_feld(feld)
            figure_sprites.update()
            step = 1
        down = True
    if keystate[pygame.K_LEFT] and action != 'down_const':
        if check_move(feld, active_figure, [-1, 0]):
            action = 'left'
            active_figure['x'] -= 1
    elif keystate[pygame.K_RIGHT] and action != 'down_const':
        if check_move(feld, active_figure, [+1, 0]):
            action = 'right'
            active_figure['x'] += 1
    all_sprites.update()
    if action == 'down_const':
        active_figure = create_figure(random.choice(list(figures_base_dict.keys())))
        if check_imposition(feld, active_figure['base'], active_figure['x'], active_figure['y'],
                            active_figure['shape']):
            running = False
    step += 1

    # Draw / render
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
