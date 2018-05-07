import pygame
import random
import time
from pygame.locals import *


pygame.init()


display_width = 1000
display_height = 800


FPS = 15
direction = "right"


# color RGB values
#         R    G    B
ORCHID = (104, 34, 139)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (178,   34,   34)
GREEN = (  0, 120,   0)
BLUE  = (  0,   0, 255) 
YELLOW = (255, 255, 0)
ORANGE = (255, 97, 3)
 
gameDisplay = pygame.display.set_mode((display_width, display_height))  # dimensions of the display
pygame.display.set_caption('Save The Horcrux')                          # game title
slytherinImage = pygame.image.load("slytherin.png").convert()           # loading image for the start screen


icon = pygame.image.load('hallows.png')
pygame.display.set_icon(icon)                      # loading an image and setting an icon


gem_sound = pygame.mixer.Sound("gem.ogg")          # sound when snake collects the gem
lion_sound = pygame.mixer.Sound("lion.wav")        # sound when snake encounters the lion

pygame.mixer.music.load("harry.ogg")               # background music
pygame.mixer.music.play(5)

img = pygame.image.load('snakehead.png')           # snakehead image
gemimg = pygame.image.load('gem.png')              # gem image
blockimg = pygame.image.load('block.png')          # block image

pygame.display.update() 

clock = pygame.time.Clock()
block_size = 30
gemThickness = 50
blockThickness = 50

# setting font type and sizes

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def pause():     # function for pausing the game
	paused = True
	message_to_screen("Paused" , RED, -100, size = "large")
	message_to_screen("Press C to continue or Q to quit", ORANGE, 25)
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()


		clock.tick(5)


def score(score):      # displays score
	text = smallfont.render("Score: "+str(score), True, YELLOW)
	gameDisplay.blit(text, [0,0])


def randGemGen():      # generates gems at random positions
	gemX = round(random.randrange(0, display_width - gemThickness)/10.0) * 10.0    # Keeping the range from 0 to display_width makes grabbing a gem at the edge difficult, hence 2 * block_size
	gemY = round(random.randrange(0, display_height - gemThickness)/10.0) * 10.0

	return gemX, gemY


def randBlockGenX_1():      # generates blocks i.e. lion at random positions (x position)
	blockX_1 = int(round(random.randrange(20, display_width - blockThickness)/20.0) * 20.0)    
	
	return blockX_1
	
def randBlockGenY_1():      # generates blocks i.e. lion at random positions (y position)
	blockY_1 = int(round(random.randrange(20, display_height - blockThickness)/20.0) * 20.0)

	return blockY_1
	

def checkOverlap(x, y):
	for i in range(int(x) - 25, int(x) + 25):
		for j in range(int(y)-25, int(y)+25):
			if gameDisplay.get_at((i, j))[0:2] == BLACK:
				return False

#MAKE BLOCK


def start_screen():  # function to load start screen
	intro = True

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		x = 0; # x coordinate of image
		y = 0; # y coordinate of image
		gameDisplay.blit(slytherinImage, ( x,y)) 
		pygame.display.flip() # paint screen one time

		pygame.display.update()
		clock.tick(15)


def snake(block_size, snakelist):   # function for generating snake and its movements

	if direction == "right":
		head = pygame.transform.rotate(img, 270)

	if direction == "left":
		head = pygame.transform.rotate(img, 90)

	if direction == "up":
		head = img

	if direction == "down":
		head = pygame.transform.rotate(img, 180)

	gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

	for element in snakelist[:-1]:
		pygame.draw.rect(gameDisplay, RED, [element[0], element[1], block_size, block_size])

# designates the size and color of text on screen
def text_objects(text, color, size):    
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)

	return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, distance = 0, size = "small"):   # for displaying messages, this function is used in other functions
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (display_width/2), (display_height/2) + distance
	gameDisplay.blit(textSurf, textRect)

		

def startGame():  # main game loop, runs the game
	global direction

	direction = "right"  # starting position of snake

	gameExit = False
	gameOver = False
 
	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 10
	lead_y_change = 0

	snakeList = []
	snakeLength = 1

	gem_space_occupied = True
	while gem_space_occupied:
		gemX, gemY = randGemGen()
		if not checkOverlap(gemX, gemY):
			gem_space_occupied = False

	# saves the x and y positions of the block object i.e. the lion
	blockX_1 = []
	blockY_1 = []

	Intersects = True
	while Intersects:
		x = randBlockGenX_1()
		y = randBlockGenY_1()
		if not checkOverlap(x, y):
			Intersects = False
 
	blockX_1.append(x)
	blockY_1.append(y)

	while not gameExit:
		if gameOver == True:
			message_to_screen("Game over!", GREEN, distance = -50, size = "large")
			message_to_screen("Press C to play again or Q to quit", ORANGE, 50, size = "medium")
			pygame.display.update()

		while gameOver == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						startGame()

# event handling loop (change in directions, pausing)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "right":
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "left":
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "down":
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "up":
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0
				elif event.key == pygame.K_p:
					pause()

		# if it hits the wall
		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
			gameOver = True
		

		lead_x += lead_x_change
		lead_y += lead_y_change
	 
		gameDisplay.fill(BLACK)
	
		gameDisplay.blit(gemimg, (gemX, gemY))
		for i in range(len(blockX_1)):
			gameDisplay.blit(blockimg, (blockX_1[i], blockY_1[i]))

		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)


		if len(snakeList) > snakeLength:
			del snakeList[0]

		# if snake runs into itself
		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True

		snake(block_size, snakeList)

		score(snakeLength-1)

		pygame.display.update()

		# gem collection
		if lead_x > gemX and lead_x < gemX + gemThickness or lead_x + block_size > gemX and lead_x + block_size < gemX + gemThickness:
			if lead_y > gemY and lead_y < gemY + gemThickness:
				pygame.mixer.Sound.play(gem_sound)
				gemX, gemY = randGemGen() # new gem creation
				if snakeLength % 5 == 0 :   # creates a new block at the collection of every five no. of gems
					blockX_1.append(randBlockGenX_1())
					blockY_1.append(randBlockGenY_1())
				
				snakeLength += 1 #snake length increase
				
			elif lead_y + block_size > gemY and lead_y + block_size < gemY + gemThickness: 
				pygame.mixer.Sound.play(gem_sound)
				gemX, gemY = randGemGen()
				if snakeLength % 5 == 0 :
					blockX_1.append(randBlockGenX_1())
					blockY_1.append(randBlockGenY_1())
				
				snakeLength += 1 
				
		# if snake hits the block object, game over
		for i in range(len(blockX_1)):
			if lead_x > blockX_1[i] and lead_x < blockX_1[i] + blockThickness or lead_x + block_size > blockX_1[i] and lead_x + block_size < blockX_1[i] + blockThickness:
				if lead_y > blockY_1[i] and lead_y < blockY_1[i] + blockThickness:
					pygame.mixer.Sound.play(lion_sound)
					gameOver = True
				elif lead_y + block_size > blockY_1[i] and lead_y + block_size < blockY_1[i] + blockThickness:
					pygame.mixer.Sound.play(lion_sound)
					gameOver = True


		clock.tick(FPS)  # frames per second (increasing processing)

	message_to_screen("Game over!", ORCHID, distance = -50, size = "large")
	pygame.display.update()
	time.sleep(2)
	pygame.quit()
	quit()	

start_screen()
startGame()
