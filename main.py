import pygame
import math
from tkinter import messagebox
from tkinter import *


def check_win(pos):
    if pos.__contains__((0, 0)) and pos.__contains__((1, 1)) and pos.__contains__((2, 2)) or pos.__contains__((0, 2)) \
            and pos.__contains__((1, 1)) and pos.__contains__((2, 0)):
        return True
    for x in range(3):
        counter_X, counter_Y = 0, 0
        for y in range(3):
            if pos.__contains__((x, y)):
                counter_X += 1
            if pos.__contains__((y, x)):
                counter_Y += 1
            if counter_X == 3 or counter_Y == 3:
                return True


def game_over_screen(winner):
    window = Tk()
    window.withdraw()
    screen = messagebox.askquestion(winner, "Do you want to restart the game?")
    if screen == "yes":
        restart = Game()
        restart.run()


class Game:
    def __init__(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.screen = pygame.display.set_mode((600, 600))
        self.size = 200
        pygame.display.set_caption('TIC TAC TOE')
        self.running = True
        self.first_move_bol = True
        self.all_pos = [(x, y) for x in range(3) for y in range(3)]
        self.positions_X = set()
        self.positions_O = set()
        self.best_positions = {}

    def grid(self):
        for pos in self.all_pos:
            pygame.draw.rect(self.screen, self.WHITE, (pos[0] * self.size, pos[1] * self.size, self.size, self.size), 1)

    def show_X(self, x, y):
        x = x * self.size
        y = y * self.size
        pygame.draw.line(self.screen, self.WHITE, (x, y), (x + self.size, y + self.size), 5)
        pygame.draw.line(self.screen, self.WHITE, (x + self.size, y), (x, y + self.size), 5)

    def show_O(self, x, y):
        radius = int(self.size / 2)
        x = x * self.size
        y = y * self.size
        pygame.draw.circle(self.screen, self.WHITE, (x + radius, y + radius), radius, 3)

    def first_move(self):
        if self.positions_X.__contains__((1, 1)):
            return 0, 0
        else:
            return 1, 1

    def best_move(self):
        self.MiniMax(0, True)
        # MiniMax will fill the self.best_positions
        if self.best_positions:
            shortest_depth_to_win = min(self.best_positions)
            ans = self.best_positions[shortest_depth_to_win]
            self.best_positions.clear()
            return ans

    def MiniMax(self, depth, is_max):
        """ I DO NOT GIVE ANY POS AS PARAMETER SO WILL TAKE THE FIRST POSITION THAT WILL WIN FOR SURE"""
        if check_win(self.positions_X):
            return -1
        elif check_win(self.positions_O):
            return 1
        elif len(self.positions_X) + len(self.positions_O) == 9:
            return 0

        #   AI TURN
        if is_max:
            best_score = -999
            for pos in self.all_pos:
                if pos not in self.positions_X and pos not in self.positions_O:
                    self.positions_O.add(pos)
                    score = self.MiniMax(depth + 1, False)
                    self.positions_O.remove(pos)
                    if score > best_score:
                        best_score = score
                        """Here is where it gets store so i can return the best pos"""
                        self.best_positions[depth] = pos
            return best_score

        #   HUMAN TURN
        else:
            best_score = 999
            for pos in self.all_pos:
                if pos not in self.positions_X and pos not in self.positions_O:
                    self.positions_X.add(pos)
                    score = self.MiniMax(depth + 1, True)
                    self.positions_X.remove(pos)
                    best_score = min(best_score, score)
            return best_score

    def run(self):
        while self.running:
            'Check game over'
            if check_win(self.positions_X):
                game_over_screen("X WON")
                return
            elif check_win(self.positions_O):
                game_over_screen("O WON")
                return
            elif len(self.positions_X) + len(self.positions_O) == 9:
                game_over_screen("ITS A TIE")
                return

            "Mouse and click settings "
            x_pos = pygame.mouse.get_pos()[0]
            y_pos = pygame.mouse.get_pos()[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x_pos = math.floor(x_pos / self.size)
                    y_pos = math.floor(y_pos / self.size)
                    if (x_pos, y_pos) not in self.positions_O:
                        self.positions_X.add((x_pos, y_pos))
            self.screen.fill(self.BLACK)
            self.grid()
            'Show X'
            for pos in self.positions_X:
                if pos not in self.positions_O:
                    self.show_X(pos[0], pos[1])

            'Selecting the next move from AI'
            if len(self.positions_X) == 1 and self.first_move_bol:
                self.positions_O.add(self.first_move())
                self.first_move_bol = False
            elif len(self.positions_X) > len(self.positions_O) and self.best_move():
                self.positions_O.add(self.best_move())

            'Show O'
            for pos in self.positions_O:
                self.show_O(pos[0], pos[1])

            pygame.display.flip()


g = Game()
g.run()
