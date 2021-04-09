import pygame
from pygame.locals import *
import sys

# Entities
NONE = 0
PLAYER = 1
AI = 2

# Size
BOARD_SIZE_H = 10
BOARD_SIZE_V = 10
TILE_SIZE = 64

# Images
NONE_BACK = pygame.image.load("none-back.png")
PLAYER_BACK = pygame.image.load("player-back.png")
AI_BACK = pygame.image.load("ai-back.png")
PLAYER_FRONT = pygame.image.load("player-front.png")
AI_FRONT = pygame.image.load("ai-front.png")

# FPS
FPS = 10

# Tile
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

	def can_move(self, direction):
		global board

		new_x = self.x + direction[0]
		new_y = self.y + direction[1]

		if (new_x > BOARD_SIZE_H - 1) or (new_x < 0):
			return False
		if (new_y > BOARD_SIZE_V - 1) or (new_y < 0):
			return False

		return board[new_y][new_x].front == NONE

# General setup
pygame.init()
pygame.display.set_caption("Esplatún 4")
screen = pygame.display.set_mode((BOARD_SIZE_H * TILE_SIZE, BOARD_SIZE_V * TILE_SIZE))
frames = pygame.time.Clock()

# Board setup
board = list()
for i in range(BOARD_SIZE_V):
	board.append(list())
	for j in range(BOARD_SIZE_H):
		board[i].append(Tile(j, i, 0, 0))

# Player setup
player = board[0][0]
player.front = PLAYER
player_direction = [1, 0]
player.draw(screen)

# AI setup
ai = board[8][8]
ai.front = AI
ai_direction = [1, 0]
ai.draw(screen)

# Move Player
def move_player(screen):
	global player
	global player_direction
	global board

	pressed_keys = pygame.key.get_pressed()

	if pressed_keys[K_UP] != pressed_keys[K_DOWN]:
		if pressed_keys[K_UP]:
			player_direction = [0, -1]
		elif pressed_keys[K_DOWN]:
			player_direction = [0, 1]
	elif pressed_keys[K_LEFT] != pressed_keys[K_RIGHT]:
		if pressed_keys[K_LEFT]:
			player_direction = [-1, 0]
		elif pressed_keys[K_RIGHT]:
			player_direction = [1, 0]

	if player.can_move(player_direction):
		new_x = player.x + player_direction[0]
		new_y = player.y + player_direction[1]
		new_tile = board[new_y][new_x]

		player.back = PLAYER
		player.front = NONE
		new_tile.front = PLAYER

		player.draw(screen)
		new_tile.draw(screen)

		player = new_tile

# Move AI
def move_ai(screen):
	global ai
	global ai_direction
	global board

	ai_direction = get_ai_direction()

	if ai.can_move(ai_direction):
		new_x = ai.x + ai_direction[0]
		new_y = ai.y + ai_direction[1]
		new_tile = board[new_y][new_x]

		ai.back = AI_BACK
		ai.front = NONE
		new_tile.front = AI

		ai.draw(screen)
		new_tile.draw(screen)

		ai = new_tile

# Get AI direction
def get_ai_direction():
	global board
	# TODO: use algorithm to get direction
	return [1, 0]

# Update funcition
def update(screen):
	move_player(screen)
	move_ai(screen)

# Game loop
while True:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	update(screen)

	frames.tick(FPS)
