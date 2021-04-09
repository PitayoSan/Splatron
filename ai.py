from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
# from test import Tile, PLAYER, AI, NONE
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
import sys
import random

# Entities
NONE = 0
PLAYER = 1
AI = 2

# Size
BOARD_SIZE_H = 8
BOARD_SIZE_V = 8
TILE_SIZE = 64

# Images
NONE_BACK = pygame.image.load("none-back.png")
PLAYER_BACK = pygame.image.load("player-back.png")
AI_BACK = pygame.image.load("ai-back.png")
PLAYER_FRONT = pygame.image.load("player-front.png")
AI_FRONT = pygame.image.load("ai-front.png")
PROGRAM_ICON = pygame.image.load('esplatun.ico')

# Colors
BLACK = (0, 0, 0)

# FPS
FPS = 15

# Music files
MATCH_TRACK = 'ost.ogg'

# Players positions
player_last = None
ai_last = None
score_last = 0

class Tile:
    def __init__(self, x, y, back, front):
        self.x = x
        self.y = y
        self.back = back
        self.front = front

    def draw(self, screen):
        image_back = None
        image_front = None

        if self.back == NONE:
            image_back = NONE_BACK
        elif self.back == PLAYER:
            image_back = PLAYER_BACK
        else:
            image_back = AI_BACK

        if self.front == NONE:
            image_front = None
        elif self.front == PLAYER:
            image_front = PLAYER_FRONT
        else:
            image_front = AI_FRONT

        screen.blit(image_back, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        if image_front:
            screen.blit(image_front, (self.x * TILE_SIZE, self.y * TILE_SIZE))


class Player:
    ALL_MOVES = [[0, -1], [0, 1], [-1, 0], [1, 0]]

    def __init__(self, board, location, entity):  # , direction):
        self.ink = 200
        self.board = board
        self.location = location  # Current Tile
        self.entity = entity
        self.location.front = self.entity
        self.prev_direction = None

    def can_move(self, direction):
        # Take current direction and see if candidate Tile is valid.
        return self.board.can_move([self.location.x + direction[0], self.location.y + direction[1]])

    def move(self, direction):
        self.prev_direction = direction

        new_x = self.location.x + direction[0]
        new_y = self.location.y + direction[1]
        new_tile = self.board.tiles[new_y][new_x]

        self.location.back = self.entity
        self.location.front = NONE
        new_tile.front = self.entity

        self.location = new_tile
        self.ink -= 1

    def possible_moves(self):
        moves = [d for d in Player.ALL_MOVES if self.can_move(d)]
        if not moves:
            return [[0, 0]]
        return moves

    def get_score(self):
        pass

class Human(Player):

    def __init__(self, board):
        super().__init__(board, board.spawn_alpha(), PLAYER)

    def get_direction(self):  # Should return valid direction

        direction = self.prev_direction
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] != pressed_keys[K_DOWN]:
            if pressed_keys[K_UP]:
                direction = [0, -1]
            elif pressed_keys[K_DOWN]:
                direction = [0, 1]
        elif pressed_keys[K_LEFT] != pressed_keys[K_RIGHT]:
            if pressed_keys[K_LEFT]:
                direction = [-1, 0]
            elif pressed_keys[K_RIGHT]:
                direction = [1, 0]

        if direction in self.possible_moves():
            return direction
        else:
            # Do nothing?
            return [0, 0]
        
    def get_score(self):
        score = 0
        for row in self.board.tiles:
            for tile in row:
                if tile.back == 1: score += 1
        
        return score


class Ai(Player):

    def __init__(self, board):
        super().__init__(board, board.spawn_beta(), AI)

    def get_direction(self):
        # Use NegaMax to return next move accoding to game's possible_moves
        return game.get_move()

    def can_move(self, direction):
        # Take current direction and see if candidate Tile is valid.
        illegal_move = [self.prev_direction[0] * -1, self.prev_direction[1] * -1]
        if illegal_move == direction:
            return False
        return super().can_move(direction)
    
    # def possible_moves(self):
    #     ai_moves = [d for d in Player.ALL_MOVES if self.can_move(d)]
    #     ai_moves.append([0, 0])
    #     return ai_moves

    def get_score(self):
        score = 0
        for row in self.board.tiles:
            for tile in row:
                if tile.back == 2: score += 1
        
        return score


class Board:

    def __init__(self, size_h, size_v):
        self.size_h = size_h
        self.size_v = size_v
        self.make_tiles()
        self.make_players()

    def make_tiles(self):
        self.tiles = list()
        for i in range(self.size_v):
            self.tiles.append(list())
            for j in range(self.size_h):
                self.tiles[i].append(Tile(j, i, 0, 0))

    def make_players(self):
        self.player_human = Human(self)
        self.player_ai = Ai(self)

    def spawn_alpha(self):
        return self.tiles[0][0]

    def spawn_beta(self):
        return self.tiles[self.size_v - 1][self.size_h - 1]

    def can_move(self, target_location):
        new_x = target_location[0]
        new_y = target_location[1]

        if (new_x > self.size_h - 1) or (new_x < 0):
            return False
        if (new_y > self.size_v - 1) or (new_y < 0):
            return False

        return self.tiles[new_y][new_x].front == NONE
    
    '''def board_score(self): # score for ai
        score = 0
        for row in self.tiles:
            for tile in row:
                if tile.back == 1: score -= 1
                elif tile.back == 2: score += 1'''

    def get_ai_score(self):
        return self.player_ai.get_score()

    def board_state(self):
        print('#######################')
        for row in self.tiles:
            for tile in row:
                print(f'{tile.back}\t', end='')
            print()
        print('#######################')
    


class Splatron(TwoPlayersGame):

    def __init__(self, players, board_size_h, board_size_v):
        self.players = players  # Array of easyAI's Player objects (easyAI stuff)
        self.board = Board(board_size_h, board_size_v)  # Create board of size h x w (Custom class)
        self.player1 = self.board.player_human  # Create Player subclass 'Human' (Custom Class)
        self.player2 = self.board.player_ai  # Create Player subclass 'Ai' (Custom class)
        self.nplayer = 1  # Set initial current player for game (easyAI stuff)

    # Return Player (Custom Class) object from game's current index.
    def current_player(self):
        return self.player1 if self.nplayer == 1 else self.player2

    def is_over(self):
        return self.player1.ink == 0 and self.player2.ink == 0

    def possible_moves(self):
        return self.current_player().possible_moves()

    def make_move(self, direction):
        # Given a valid direction, move the player
        self.current_player().move(direction)

    def scoring(self):
        score = self.player2.get_score() - self.player1.get_score()
        return score
    
    def scoreboard(self):
        return f'HUMAN: {str(self.player1.get_score())} ({str(self.player1.ink)})  AI: {str(self.player2.get_score())} ({str(self.player2.ink)})'


# General setup
pygame.init()

# Music Mixer
pygame.mixer.init()
pygame.mixer.music.load(MATCH_TRACK)
pygame.mixer.music.play(-1)

# Window elements
pygame.display.set_caption("Splatron")
pygame.display.set_icon(PROGRAM_ICON)

# Screen
screen = pygame.display.set_mode((BOARD_SIZE_H * TILE_SIZE, BOARD_SIZE_V * TILE_SIZE + 35))
frames = pygame.time.Clock()

# Game
game = Splatron([Human_Player(), AI_Player(Negamax(4))], BOARD_SIZE_H, BOARD_SIZE_V)

# Make initial directions for each player (turns are switched automatically):
game.player1.location.draw(screen)
game.player2.location.draw(screen)

game.play_move([1, 0])  # Human player moves right
game.play_move([-1, 0])  # Ai player moves left

game.board.spawn_alpha().draw(screen)
game.board.spawn_beta().draw(screen)

game.player1.location.draw(screen)
game.player2.location.draw(screen)


def update():
    global score_last
    score_last = game.player2.get_score() - game.player1.get_score()

    global player_last
    player_last = game.current_player().location
    game.play_move(game.current_player().get_direction())
    player_last.draw(screen)
    game.player1.location.draw(screen)

    global ai_last
    ai_last = game.current_player().location
    game.play_move(game.current_player().get_direction())
    ai_last.draw(screen)
    game.player2.location.draw(screen)

    print(game.scoreboard())

    rect = pygame.Rect((1, 520, 520, 30))
    large_font = pygame.font.Font('Paintball.ttf', 20)
    text = large_font.render(
        f'HUMAN: Score {str(game.player1.get_score())} Ink {str(game.player1.ink)}%  AI: Score {str(game.player2.get_score())} Ink {str(game.player2.ink)}%',
        1,
        (255, 255, 255)
    )
    pygame.draw.rect(screen, BLACK, rect)
    screen.blit(text, rect)


while not game.is_over():
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    update()
    frames.tick(FPS)