import datetime
import pygame
from flask import Flask, request, url_for, redirect, make_response, session
from roll import dice
from config import secret_key

app = Flask("The Side Of Pety Tactics")
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = secret_key


@app.route('/red_roll', methods=["POST", "GET"])
def check_valid():
    if request.method == "POST":
        if current_player == "First":
            roll()


def get_current_player():
    return current_player


def swap():
    global current_player
    if current_player == "First":
        current_player = "Second"
    else:
        current_player = "First"


def roll():
    global current_score1, current_score2
    if get_current_player() == "First":
        current_score1 += dice(maximum1)

    else:
        current_score2 += dice(maximum2)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['b'] * width for _ in range(height)]
        self.board[0][0] = 'r'
        self.board[-1][-1] = 'p'

        self.left = 0
        self.top = 0
        self.cell_size = 75

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sc):
        color = [(220, 52, 52), (40, 65, 250), (0, 0, 0), (150, 35, 35), (36, 17, 130)]
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(sc, (230, 230, 230), (self.left + x * self.cell_size, self.top + y * self.
                                                       cell_size, self.cell_size, self.cell_size), 1)

                if self.board[y][x] == 'r':
                    pygame.draw.rect(sc, color[0],
                                     (self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1,
                                      self.cell_size-2, self.cell_size-2), 0)

                elif self.board[y][x] == 'p':
                    pygame.draw.rect(sc, color[1],
                                     (self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1,
                                      self.cell_size-2, self.cell_size-2), 0)

                elif self.board[y][x] == 'ur':
                    pygame.draw.rect(sc, color[3],
                                     (self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1,
                                      self.cell_size-2, self.cell_size-2), 0)

                elif self.board[y][x] == 'up':
                    pygame.draw.rect(sc, color[4],
                                     (self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1,
                                      self.cell_size-2, self.cell_size-2), 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_click2(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_rightclick(cell)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        nx = (x - self.left) // self.cell_size
        ny = (y - self.top) // self.cell_size
        if 0 <= nx < self.width and 0 <= ny < self.height:
            return nx, ny
        else:
            return None

    def on_click(self, cell_coords):
        global current_score1, current_score2
        if cell_coords is not None:
            x, y = cell_coords

            for i in range(self.width):
                for j in range(self.height):
                    if x == i and y == j:
                        if get_current_player() == "First":
                            if ((self.board[y][x - 1] == 'r' or self.board[y][x - 1] == 'ur') and x > -1) or \
                                    ((self.board[y - 1][x] == 'r' or self.board[y - 1][x] == 'ur') and y > -1):
                                if current_score1 >= 1 and self.board[y][x] == 'b':
                                    self.board[j][i] = 'r'
                                    current_score1 -= 1

                                elif current_score1 >= 2 and self.board[y][x] == 'p':
                                    self.board[j][i] = 'r'
                                    current_score1 -= 2

                                elif current_score1 >= 3 and self.board[y][x] == 'up':
                                    self.board[j][i] = 'r'
                                    current_score1 -= 3

                            if y < self.height - 1:
                                if self.board[y + 1][x] == 'r' or self.board[y + 1][x] == 'ur':
                                    if current_score1 >= 1 and self.board[y][x] == 'b':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 1

                                    elif current_score1 >= 2 and self.board[y][x] == 'p':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 2

                                    elif current_score1 >= 3 and self.board[y][x] == 'up':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 3

                            if x < self.width - 1:
                                if self.board[y][x + 1] == 'r' or self.board[y][x + 1] == 'ur':
                                    if current_score1 >= 1 and self.board[y][x] == 'b':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 1

                                    elif current_score1 >= 2 and self.board[y][x] == 'p':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 2

                                    elif current_score1 >= 3 and self.board[y][x] == 'up':
                                        self.board[j][i] = 'r'
                                        current_score1 -= 3

                        else:
                            if ((self.board[y][x - 1] == 'p' or self.board[y][x - 1] == 'up') and x > -1) or \
                                    ((self.board[y - 1][x] == 'p' or self.board[y - 1][x] == 'up') and y > -1):
                                if current_score2 >= 1 and self.board[y][x] == 'b':
                                    self.board[j][i] = 'p'
                                    current_score2 -= 1

                                elif current_score2 >= 2 and self.board[y][x] == 'r':
                                    self.board[j][i] = 'p'
                                    current_score2 -= 2

                                elif current_score2 >= 3 and self.board[y][x] == 'ur':
                                    self.board[j][i] = 'p'
                                    current_score2 -= 3

                            if y < self.height - 1:
                                if self.board[y + 1][x] == 'p' or self.board[y + 1][x] == 'up':
                                    if current_score2 >= 1 and self.board[y][x] == 'b':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 1

                                    elif current_score2 >= 2 and self.board[y][x] == 'r':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 2

                                    elif current_score2 >= 3 and self.board[y][x] == 'ur':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 3

                            if x < self.width - 1:
                                if self.board[y][x + 1] == 'p' or self.board[y][x + 1] == 'up':
                                    if current_score2 >= 1 and self.board[y][x] == 'b':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 1

                                    elif current_score2 >= 2 and self.board[y][x] == 'r':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 2

                                    elif current_score2 >= 3 and self.board[y][x] == 'ur':
                                        self.board[j][i] = 'p'
                                        current_score2 -= 3

    def on_rightclick(self, cell_coords):
        global current_score1, current_score2
        if cell_coords is not None:
            x, y = cell_coords

            for i in range(self.width):
                for j in range(self.height):
                    if x == i and y == j:
                        if get_current_player() == "First":
                            if (self.board[y][x - 1] == 'r' and x > -1) or (self.board[y - 1][x] == 'r' and y > -1):
                                if current_score1 >= 3 and self.board[y][x] == 'r':
                                    self.board[j][i] = 'ur'
                                    current_score1 -= 3

                            if y < self.height - 1:
                                if self.board[y + 1][x] == 'r':
                                    if current_score1 >= 3 and self.board[y][x] == 'r':
                                        self.board[j][i] = 'ur'
                                        current_score1 -= 3

                            if x < self.width - 1:
                                if self.board[y][x + 1] == 'r':
                                    if current_score1 >= 3 and self.board[y][x] == 'r':
                                        self.board[j][i] = 'ur'
                                        current_score1 -= 3

                        else:
                            if (self.board[y][x - 1] == 'p' and x > -1) or (self.board[y - 1][x] == 'p' and y > -1):
                                if current_score2 >= 3 and self.board[y][x] == 'p':
                                    self.board[j][i] = 'up'
                                    current_score2 -= 3

                            if y < self.height - 1:
                                if self.board[y + 1][x] == 'p':
                                    if current_score2 >= 3 and self.board[y][x] == 'p':
                                        self.board[j][i] = 'up'
                                        current_score2 -= 3

                            if x < self.width - 1:
                                if self.board[y][x + 1] == 'p':
                                    if current_score2 >= 3 and self.board[y][x] == 'p':
                                        self.board[j][i] = 'up'
                                        current_score2 -= 3


if __name__ == '__main__':
    pygame.init()
    app.run()
    size = (500, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The Side Of Pety Tactics v1.0')

    board = Board(20, 20)
    board.set_view(0, 50, 25)
    board.render(screen)

    font = pygame.font.SysFont('Times New Roman', 24)
    version = font.render('v1.0', True, (255, 255, 255))

    current_score1 = 0
    current_score2 = 0

    maximum1 = 3
    maximum2 = 3

    swap_button = pygame.Rect(215, 10, 80, 30)
    swap_render = font.render("Далее", True, (255, 255, 255))

    dice_button = pygame.Rect(190, 560, 120, 30)
    dice_render = font.render("Крутить", True, (255, 255, 255))

    current_player = "First"

    running = True

    next_step = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not next_step:
                        board.get_click(event.pos)
                        if swap_button.collidepoint(pygame.mouse.get_pos()):
                            swap()
                            next_step = True
                    else:
                        if dice_button.collidepoint(pygame.mouse.get_pos()):
                            roll()
                            next_step = False

                if event.button == 3:
                    if not next_step:
                        board.get_click2(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        screen.blit(version, (450, 560))
        screen.blit(font.render(str(current_score1), True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(str(current_score2), True, (255, 255, 255)), (450, 10))
        pygame.draw.rect(screen, (25, 180, 25), swap_button)
        screen.blit(swap_render, (225, 10))

        if next_step:
            pygame.draw.rect(screen, (25, 180, 25), dice_button)
            screen.blit(dice_render, (205, 560))
        if current_player == "First":
            pygame.draw.rect(screen, (220, 52, 52), (100, 10, 30, 30))
        else:
            pygame.draw.rect(screen, (36, 17, 130), (360, 10, 30, 30))
        pygame.display.flip()
    pygame.quit()
