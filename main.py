import pygame
import random
import sys


masLength = masHeight = 4    # Array size (4х4)


# Transforming list to array (4x4):
def massive(a):
    b = []
    for i in range(masLength):
        if i % 2 == 0:
            b.append(a[i*masLength:i*masLength + masLength])
        else:
            b.append(a[i*masLength + masLength - 1:i*masLength - 1:-1])
    return b


# Checking if it is possible to assemble "15 puzzle":
def isGood(a):
    n = 0
    for i in range(len(a) - 1):
        if a[i] == 0:
            continue
        for j in range(i + 1, len(a)):
            if a[j] == 0:
                continue
            if a[i] > a[j]:
                n += 1
    if n % 2 != 0:
        return True
    return False


# Creating randomly shuffled and POSSIBLE to assemble "15 puzzle" array:
def puzzle_shuffle():
    a = list(range(masLength*masHeight))
    random.shuffle(a)
    if isGood(a):
        return massive(a)
    else:
        if a[-1] == 0:
            a[-2], a[-3] = a[-3], a[-2]
        elif a[-2] == 0:
            a[-1], a[-3] = a[-3], a[-1]
        else:
            a[-1], a[-2] = a[-2], a[-1]
        return massive(a)


# Moving block to the empty space:
def move(a, row_change, column_change):
    for i in range(masLength):
        if 0 in a[i]:
            n = a[i].index(0)
            a[i][n], a[i + row_change][n + column_change] = a[i + row_change][n + column_change], a[i][n]
            return a

# Moving block left to the empty space:
def move_left(a):
    return move(a, row_change=0, column_change=1)

# Moving block right to the empty space:
def move_right(a):
    return move(a, row_change=0, column_change=-1)

# Moving block up to the empty space:
def move_up(a):
    return move(a, row_change=1, column_change=0)

# Moving block down to the empty space:
def move_down(a):
    return move(a, row_change=-1, column_change=0)


if __name__ == '__main__':
    pygame.init()
    img1 = pygame.image.load('image1.png')  # Logo to the window panel
    img2 = pygame.image.load('image2.png')  # Image for passive game area design
    movement_sound = pygame.mixer.Sound('1.wav')  # Blocks moving sound
    shuffle_sound = pygame.mixer.Sound('2.wav')  # Shuffle sound

    pygame.mixer.Sound.set_volume(movement_sound, 0.07)
    pygame.mixer.Sound.set_volume(shuffle_sound, 0.6)

    # Colors in RGB:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY1 = (195, 195, 195)

    # Fonts:
    font1 = pygame.font.SysFont('arial', 46, bold=True)
    font2 = pygame.font.SysFont('timesnewroman', 22, italic=True)
    font3 = pygame.font.SysFont('timesnewroman', 28)

    # Text to the passive game area design:
    text_press = font2.render('press', 0, WHITE)
    text_space = font3.render('Space', 0, WHITE)
    text_to = font2.render('to', 0, WHITE)
    text_shuffle = font3.render('SHUFFLE', 0, WHITE)

    # Dictionary for visualizing array's values:
    d = [
        [1, font1.render('1', 1, BLACK)],
        [2, font1.render('2', 1, BLACK)],
        [3, font1.render('3', 1, BLACK)],
        [4, font1.render('4', 1, BLACK)],
        [5, font1.render('5', 1, BLACK)],
        [6, font1.render('6', 1, BLACK)],
        [7, font1.render('7', 1, BLACK)],
        [8, font1.render('8', 1, BLACK)],
        [9, font1.render('9', 1, BLACK)],
        [10, font1.render('10', 1, BLACK)],
        [11, font1.render('11', 1, BLACK)],
        [12, font1.render('12', 1, BLACK)],
        [13, font1.render('13', 1, BLACK)],
        [14, font1.render('14', 1, BLACK)],
        [15, font1.render('15', 1, BLACK)]
    ]
    d = dict(d)

    # Defining blocks number, blocks size, margin and etc:
    BLOCKS = 4
    SIZE_BLOCK = 93
    MARGIN = 7
    EDGE_MARGIN = 4
    UP_BLOCK = 140
    DOWN_BLOCK = 90

    # Game window size:
    WIDTH = SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1) + EDGE_MARGIN * 2
    HEIGH = UP_BLOCK + SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1) + DOWN_BLOCK

    # Creating active game area:
    GAME_AREA = pygame.Rect(EDGE_MARGIN, UP_BLOCK, SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1),
                            SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1))

    screen = pygame.display.set_mode((WIDTH, HEIGH))
    pygame.display.set_caption('')
    pygame.display.set_icon(img1)

    # Creating assembled "15 puzzle" array:
    mas = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and all(map(lambda x: x[-1], mas)):
                    pygame.mixer.Sound.play(movement_sound)
                    mas = move_left(mas)
                elif event.key == pygame.K_RIGHT and all(map(lambda x: x[0], mas)):
                    pygame.mixer.Sound.play(movement_sound)
                    mas = move_right(mas)
                elif event.key == pygame.K_UP and all(map(lambda x: x, mas[-1])):
                    pygame.mixer.Sound.play(movement_sound)
                    mas = move_up(mas)
                elif event.key == pygame.K_DOWN and all(map(lambda x: x, mas[0])):
                    pygame.mixer.Sound.play(movement_sound)
                    mas = move_down(mas)
                elif event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(shuffle_sound)
                    mas = puzzle_shuffle()
        screen.blit(img2, (-4, 0)) # Designing passive game area
        pygame.draw.rect(screen, WHITE, GAME_AREA) # Drawing game area on the screen that is broken into square blocks:
        for j in range(1, BLOCKS):
            x = EDGE_MARGIN + SIZE_BLOCK*j + MARGIN*(j - 1)
            y = UP_BLOCK
            pygame.draw.rect(screen, GREY1, (x, y, MARGIN, SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1)))
        for i in range(1, BLOCKS):
            x = EDGE_MARGIN
            y = UP_BLOCK + SIZE_BLOCK*i + MARGIN*(i - 1)
            pygame.draw.rect(screen, GREY1, (x, y, SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1), MARGIN))
        # Paint grey '0 value' block and visualizing other array's values:
        for i in range(BLOCKS):
            for j in range(BLOCKS):
                if mas[i][j] == 0:
                    pygame.draw.rect(screen, GREY1, (EDGE_MARGIN + (SIZE_BLOCK + MARGIN)*j, UP_BLOCK +
                                                     (SIZE_BLOCK + MARGIN)*i, SIZE_BLOCK, SIZE_BLOCK))
                else:
                    text_rect = d[mas[i][j]].get_rect(center=(EDGE_MARGIN + (SIZE_BLOCK + MARGIN)*j + int(SIZE_BLOCK/2),
                                                              UP_BLOCK + (SIZE_BLOCK + MARGIN)*i + int(SIZE_BLOCK/2)))
                    screen.blit(d[mas[i][j]], text_rect)
        screen.blit(text_press, (39, 564)) # Designing passive game area
        screen.blit(text_space, (105, 560))
        screen.blit(text_to, (196, 564))
        screen.blit(text_shuffle, (236, 561))
        pygame.display.update()
