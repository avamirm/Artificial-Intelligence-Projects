from select import select
# from symbol import dotted_as_name

import turtle
import math
import random
from time import sleep
from sys import argv
from copy import deepcopy 
import time
class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        # self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        # sleep(1)
    
    def _swap_turn(self, turn):
        if turn == 'red':
            return 'blue'
        if turn == 'blue':
            return 'red'
        return None
    def _evaluate(self):
        gameoverValue = self.gameover(self.red, self.blue)
        if gameoverValue == 'red':
            return math.inf
        if gameoverValue == 'blue':
            return -math.inf
        movesWithoutTriangle = 0
        for move in deepcopy(self.available_moves):
            if self.turn == 'red':
                self.red.append(move)
                self.available_moves.remove(move)
                gameoverValue = self.gameover(self.red, self.blue)
                if gameoverValue == 0:
                    movesWithoutTriangle += 4
                if gameoverValue == 'blue':
                     movesWithoutTriangle -= 2
                self.red.remove(move)
                self.available_moves.append(move)
            else:
                self.blue.append(move)
                self.available_moves.remove(move)
                gameoverValue = self.gameover(self.red, self.blue)
                if gameoverValue == 0:
                    movesWithoutTriangle -= 4
                if gameoverValue == 'red':
                     movesWithoutTriangle += 2
                self.blue.remove(move)
                self.available_moves.append(move)
        return movesWithoutTriangle

    def minimax(self, depth, player_turn, alpha, beta):
        if depth == 0 or len(self.available_moves) == 0:
            return None, self._evaluate(), depth
        best_move = None
        best_move_depth = math.inf
        if player_turn == 'red':
            best_score = -math.inf
        else:
            best_score = math.inf
        for move in deepcopy(self.available_moves):
            self.available_moves.remove(move)
            if player_turn == 'red':
                self.red.append(move)
            else:
                self.blue.append(move)
            self.turn = self._swap_turn(self.turn)
            _, score , depth_= self.minimax(depth - 1, self.turn, alpha, beta)
            self.available_moves.append(move)
            if player_turn == 'red':
                self.red.remove(move)
            else:
                self.blue.remove(move)
            self.turn = self._swap_turn(self.turn)
            if player_turn == 'red':
                if score > best_score or (score == best_score and depth_ < best_move_depth):
                    best_move_depth = depth_
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                if score < best_score or (score == best_score and depth_ < best_move_depth):
                    best_move_depth = depth_
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
            if self.prune and beta <= alpha:
                break
        return best_move, best_score, best_move_depth
        
    def enemy(self):
        return random.choice(self.available_moves)

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                alpha = -math.inf
                beta = math.inf
                selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn, alpha=alpha, beta=beta)[0]
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    dotSet = set()
                    dotSet.update(r[i])
                    dotSet.update(r[j])
                    dotSet.update(r[k])
                    if len(dotSet) == 3:
                        return 'blue'

        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    dotSet = set()
                    dotSet.update(b[i])
                    dotSet.update(b[j])
                    dotSet.update(b[k])
                    if len(dotSet) == 3:
                        return 'red'

        return 0


if __name__=="__main__":


    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    results = {"red": 0, "blue": 0}
    time_sum = 0
    n = 100
    for i in range(n):
        start = time.time()
        results[game.play()] += 1 
        time_sum += time.time() - start  
    print(f'game played for {n} times')
    print(results)
    print(f'Algorithm time: {time_sum/n}') 
    print(f'winning probability: {results["red"]/n}')
    