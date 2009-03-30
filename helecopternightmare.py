import pygame, random
from pygame.locals import *

class thing():
	def __init__(self, x, y, h, w):
		self.x = x
		self.y = y
		self.xvel = 0
		self.yvel = 0
		self.h = h
		self.w = w
		self.dead = 0
	
	def rect(self):
		return pygame.rect.Rect(self.x, self.y, self.w, self.h)

	def collision(self, other):
		return self.rect().colliderect(other.rect())

	def show(self, screen, sprite, cam):
		screen.blit(sprite, (self.x - cam.x, self.y))

class player(thing):
	def update(self, ufos, world, cam):
		dx, dy = pygame.mouse.get_rel()
		self.xvel = 16 
		self.yvel = dy
		self.x += self.xvel
		self.y += self.yvel
		if cam.rect().contains(self.rect()) == False:
			self.x -= self.xvel
			self.y -= self.yvel

		for i in world:
			if cam.rect().contains(i.rect()):
				if self.collision(i):
					self.dead = 1
		for i in ufos:
			if cam.rect().contains(i.rect()):
				if self.collision(i):
					self.dead = 1

class ufo(thing):
	def update(self, world, lasers, cam):
		self.yvel = random.randint(-16,16)
		self.y += self.yvel
		for i in world:
			if cam.rect().contains(i.rect()):
				if self.collision(i):
					self.y -= self.yvel
		for i in lasers:
			if cam.rect().contains(i.rect()):
				if self.collision(i):
					self.dead = 1
					i.dead = 1

class laser(thing):
	def update(self, ufos, world, cam):
		self.x += self.xvel
		for i in world:
			if cam.rect().contains(i.rect()):
				if self.collision(i):
					self.dead = 1

class camera():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.h = 600
		self.w = 800
	def update(self):
		self.x += 16
	def rect(self):
		return pygame.rect.Rect(self.x, self.y, self.w, self.h)

def loadworld(file):
	#Reads in level data from a .pbm image file. A black pixel stands for a rock; a white pixel is empty space.
	#We try to go easy on the rocks or the game runs sloooooow, but avoid a case where you can go off top or bottom of screen.
	world = []
	f = open(file, 'r')
	f.readline()
	f.readline()
	scale = f.readline()
	xmax, sep, ymax = scale.partition(' ')
	xmax = int(xmax)
	ymax = int(ymax)
	s = f.read(1)
	for y in range(ymax):
		for x in range(xmax):
			repeat = 1
			while repeat == 1:
				if s == '1':
					newrock = thing(x*32, y*32, 32, 32)
					world.append(newrock)
					repeat = 0
				elif s == '0':
					repeat = 0
				else:
					repeat = 1
				s = f.read(1)
	f.close()
	return world

def loadufos(file):
	#Also reads a .pbm image, same format as for rocks. A black pixel is a UFO. It's best to keep them around 800 pixels apart, about twenty altogether.
	#GIMP is our level editor!
	ufos = []
	f = open(file, 'r')
	f.readline()
	f.readline()
	scale = f.readline()
	xmax, sep, ymax = scale.partition(' ')
	xmax = int(xmax)
	ymax = int(ymax)
	s = f.read(1)
	for y in range(ymax):
		for x in range(xmax):
			repeat = 1
			while repeat == 1:
				if s == '1':
					newufo = ufo(x*32, y*32, 23, 32)
					ufos.append(newufo)
					repeat = 0
				elif s == '0':
					repeat = 0
				else:
					repeat = 1
				s = f.read(1)
	f.close()
	return ufos


def main():
	random.seed()
	pygame.init()
	pygame.mouse.set_visible(False)
	screen = pygame.display.set_mode((800,600), FULLSCREEN)
	cam = camera()
	world = loadworld('data/map/helecopternightmare/world.pbm')
	ufos = loadufos('data/map/helecopternightmare/ufos.pbm')
	lasers = []
	you = player(128, 300, 16, 32)
	helesprite = pygame.image.load("data/images/helecopternightmare/hele.png").convert_alpha()
	ufosprite = pygame.image.load("data/images/helecopternightmare/ufo.png").convert_alpha()
	lasersprite = pygame.image.load("data/images/helecopternightmare/laser.png").convert_alpha()
	rocksprite = pygame.image.load("data/images/helecopternightmare/rock.png").convert()
	while you.dead == 0:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				#Shoot a laser if any mousebutton is clicked. We try to keep 4 on screen at maximum.
				newlaser = laser(you.x + 33, you.y + 16, 2, 16)
				newlaser.xvel = you.xvel + 4
				lasers.append(newlaser)
				if len(lasers) > 4:
					lasers.remove(lasers[0])
		you.update(ufos, world, cam)
		cam.update()
		for i in lasers:
			if cam.rect().contains(i.rect()):
				#For speed, only update objects if they are on screen.
				i.update(ufos, world, cam)
			if i.dead == 1:
				lasers.remove(i)
		for i in ufos:
			if cam.rect().contains(i.rect()):
				i.update(world, lasers, cam)
			if i.dead == 1:
				ufos.remove(i)

		pygame.draw.rect(screen,(0,0,0),(0,0,800,600))
		you.show(screen, helesprite, cam)
		for i in ufos:
			if cam.rect().contains(i.rect()):
				i.show(screen, ufosprite, cam)
		for i in lasers:
			if cam.rect().contains(i.rect()):
				i.show(screen, lasersprite, cam)
		for i in world:
			if cam.rect().contains(i.rect()):
				i.show(screen, rocksprite, cam)
		pygame.display.flip()
	return 20 - len(ufos)

print main()

