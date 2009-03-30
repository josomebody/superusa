import pygame
from pygame.locals import *

class balloon():
	def __init__(self, x, y, frame):
		self.x = x
		self.y = y
		self.frame = frame
		self.size = 0
	def grow(self):
		self.size += 5
		if self.size > 100:
			self.size = 100 
	def shrink(self):
		if self.size > 0:
			self.size -= 1
	def show(self, screen):
		cframe = self.size / 10
		screen.blit(self.frame[cframe], (self.x, self.y))


def main():
	#Not much to say here. This game is nigh perfect, though it may hurt to play on faster machines.
	pygame.init()
	screen = pygame.display.set_mode((800, 600),FULLSCREEN)
	pygame.mouse.set_visible(False)
	time = 600
	frames = []
	for i in range(11):
		frames.append(pygame.image.load("data/images/pushbuttonfastascan/balloon" + str(i) + ".png").convert_alpha())
	you = balloon(0, 0, frames)
	bg = pygame.image.load("data/images/pushbuttonfastascan/bg.png").convert()
	title = [pygame.image.load("data/images/pushbuttonfastascan/title0.png").convert(), pygame.image.load("data/images/pushbuttonfastascan/title1.png").convert()]
	tc = 0
	while time > 0:
		you.shrink()
		showtitle = 1
		if tc == 0:
			tc = 1
		else:
			tc = 0

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					you.grow()
					showtitle = 0
		time -= 1
		screen.blit(bg, (0,0))
		pygame.draw.rect(screen, (255, 0, 0), (0,0,10,time))
		you.show(screen)
		if showtitle == 1:
			screen.blit(title[tc],(0,0))
		pygame.display.flip()
	return you.size / 5

print main()
