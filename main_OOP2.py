import pygame
import random
import sys


# Defining blocks number, blocks size, margin and etc:
masLength = masHeight = BLOCKS = 4
SIZE_BLOCK = 93
MARGIN = 7
EDGE_MARGIN = 4
UP_BLOCK = 140
DOWN_BLOCK = 90

# Colors in RGB:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (195, 195, 195)


class Block:
    size = SIZE_BLOCK

    def __init__(self, number):
        if number == 16:
            self.number = ''
            self.color = GREY
        else:
            self.number = number
            self.color = WHITE


class Puzzle:
    def __init__(self):
        self.container = {}
        for i in range(1, 17):
            self.container[i] = Block(i)

    @property
    def empty_position(self):
        for key in self.container:
            if self.container[key].number == '':
                return key

    def move(self, empty_position, key_change):
        self.container[empty_position], self.container[empty_position + key_change] = \
            self.container[empty_position + key_change], self.container[empty_position]

    def move_left(self):
        self.move(self.empty_position, 1)

    def move_right(self):
        self.move(self.empty_position, -1)

    def move_up(self):
        self.move(self.empty_position, 4)

    def move_down(self):
        self.move(self.empty_position, -4)

    def shuffle(self):
        a = list(range(1, masLength * masHeight + 1))
        random.shuffle(a)
        n = 0
        for i in range(len(a) - 1):
            if a[i] == 16:
                continue
            for j in range(i + 1, len(a)):
                if a[j] == 16:
                    continue
                if a[i] > a[j]:
                    n += 1
        if n % 2 == 0:
            if a[-1] == 16:
                a[-2], a[-3] = a[-3], a[-2]
            elif a[-2] == 16:
                a[-1], a[-3] = a[-3], a[-1]
            else:
                a[-1], a[-2] = a[-2], a[-1]
        b = []
        self.container = {}
        for i in range(masLength):
            if i % 2 == 0:
                b.append(a[i * masLength:i * masLength + masLength])
            else:
                b.append(a[i * masLength + masLength - 1:i * masLength - 1:-1])
        for i in range(len(b)):
            for j in range(len(b[i])):
                self.container[i * masLength + j + 1] = Block(b[i][j])


# Game window size:
WIDTH = SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1) + EDGE_MARGIN * 2
HEIGH = UP_BLOCK + SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1) + DOWN_BLOCK

# Active game area:
GAME_AREA = pygame.Rect(EDGE_MARGIN, UP_BLOCK, SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1),
                        SIZE_BLOCK * BLOCKS + MARGIN * (BLOCKS - 1))

screen = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption('15 PUZZLE')


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    movement_sound = pygame.mixer.Sound('1.wav')  # Blocks moving sound
    shuffle_sound = pygame.mixer.Sound('2.wav')  # Shuffle sound

    pygame.mixer.Sound.set_volume(movement_sound, 0.07)
    pygame.mixer.Sound.set_volume(shuffle_sound, 0.6)

    # Fonts:
    font1 = pygame.font.SysFont('arial', 46, bold=True)
    font2 = pygame.font.SysFont('timesnewroman', 22, italic=True)
    font3 = pygame.font.SysFont('timesnewroman', 28)

    # Text to the passive game area design:
    text_rules_1 = font3.render('Shuffle puzzle and assemble', 0, WHITE)
    text_rules_2 = font3.render('numbers in the right order', 0, WHITE)
    text_press = font2.render('press', 0, WHITE)
    text_space = font3.render('Space', 0, WHITE)
    text_to = font2.render('to', 0, WHITE)
    text_shuffle = font3.render('SHUFFLE', 0, WHITE)

    puzzle = Puzzle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if puzzle.empty_position % 4 != 0:
                        puzzle.move_left()
                        pygame.mixer.Sound.play(movement_sound)
                elif event.key == pygame.K_RIGHT:
                    if puzzle.empty_position % 4 != 1:
                        puzzle.move_right()
                        pygame.mixer.Sound.play(movement_sound)
                elif event.key == pygame.K_UP:
                    if (puzzle.empty_position - 1) // 4 != 3:
                        puzzle.move_up()
                        pygame.mixer.Sound.play(movement_sound)
                elif event.key == pygame.K_DOWN:
                    if (puzzle.empty_position - 1) // 4 != 0:
                        puzzle.move_down()
                        pygame.mixer.Sound.play(movement_sound)
                elif event.key == pygame.K_SPACE:
                    puzzle.shuffle()
                    pygame.mixer.Sound.play(shuffle_sound)
        pygame.draw.rect(screen, GREY, GAME_AREA) # Drawing active game area with blocks on the screen:

        for key in puzzle.container:
            block_AREA = pygame.Rect(EDGE_MARGIN + (Block.size + MARGIN) * ((key - 1) % 4), UP_BLOCK + (Block.size
                        + MARGIN) * ((key - 1) // 4), Block.size, Block.size)
            pygame.draw.rect(screen, puzzle.container[key].color, block_AREA)
            text_rect = font1.render(str(puzzle.container[key].number), 1, BLACK).get_rect(center=(EDGE_MARGIN +
                        (Block.size + MARGIN) * ((key - 1) % 4) + int(Block.size / 2), UP_BLOCK + (Block.size +
                        MARGIN) * ((key - 1) // 4) + int(Block.size / 2)))
            screen.blit(font1.render(str(puzzle.container[key].number), 1, BLACK), text_rect)

        screen.blit(text_rules_1, (40, 30)) # Designing passive game area
        screen.blit(text_rules_2, (53, 70))
        screen.blit(text_press, (39, 564))
        screen.blit(text_space, (105, 560))
        screen.blit(text_to, (196, 564))
        screen.blit(text_shuffle, (236, 561))
        pygame.display.update()
