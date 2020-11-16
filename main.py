import pygame
pygame.init()
screen = pygame.display.set_mode((500, 500))
done = False

pygame.display.set_caption('Tetris')
icon = pygame.image.load(r'pictures/icon.png')
pygame.display.set_icon(icon)

image = pygame.image.load(r'pictures/background.jpg')
screen.blit(image, (0,0))


pygame.mixer.music.load(r'music/gameBackground.mp3')
pygame.mixer.music.play(-1)

x=60
y=60

while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 90, 90))
        pygame.display.flip()
