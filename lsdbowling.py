import pygame, math, random
from pygame.locals import *

def toxy(x, y, z):
	#If you're really bored, come up with a better perspective code. This one sucks.
	sx = 400 + x * 600  / (z + 600) 
	sy = 300 - y * 800  / (z + 600)
	return (sx, sy)

def collision(guy1, guy2):
	#Lazy 3d collision detection. Really slow. Most of this code actually sucks.
	xdist = guy1.x - guy2.x
	zdist = guy1.z - guy2.z
	distance = math.sqrt(xdist**2 + zdist**2)
	if (distance <= (guy1.r + guy2.r)):
		return 1
	else:
		return 0

class pin():
	def __init__(self, x, z):
		self.x = x
		self.z = z
		self.y =0 #You may need to change this to keep them on the floor if you mess with the perspective code.
		self.h = 71
		self.r = 16
		self.set = 1
		self.cframe = 0
		self.frame = []
		for num in range(1, 10):
			#Might be faster to just load the images from disk once and reuse the image objects. Whatever.
			frame = pygame.image.load("data/images/lsdbowling/pin" + str(num) + ".png").convert_alpha()
			self.frame.append(frame)

	def fall(self, time):
		#This code needs to be made less processor speed dependent and use a real clock.
		if (self.set == 1):
			self.set = 0
			self.fallstart = time
		else:
			if (self.cframe < 8):
				if (time - self.fallstart >=2):
					self.fallstart = time
					self.cframe += 1

	def show(self, screen):
		#screen.blit(pygame.transform.scale(self.frame[self.cframe], (self.r/(self.z/self.r)*10, self.h/(self.z/self.h)*10)), toxy(self.x, self.y, self.z))
		screen.blit(self.frame[self.cframe], toxy(self.x, self.y, self.z))

class ball():
	def __init__(self):
		self.x = 0
		self.z = 96
		self.y = 0
		self.r = 48
		self.frame = pygame.image.load("data/images/lsdbowling/ball.png").convert_alpha()

	def reset(self):
		self.x = 0
		self.z = 96
		self.y = -200

	def setup(self, dx, dy):
		self.x += dx
		self.y += dy

	def bowl(self, power, angle):
		if (self.y > 0):
			self.y -= 1
		self.z += power
		self.x += angle

	def show(self, screen):
		screen.blit(pygame.transform.scale(self.frame, ((self.r/(self.z/self.r))*10, (self.r/(self.z/self.r))*10)), toxy(self.x, self.y, self.z))

def main():
	random.seed()
	pygame.init()
	pygame.mouse.set_visible(False)
	font = pygame.font.SysFont("Terminal", 14)
	screen = pygame.display.set_mode((800,600),FULLSCREEN)
	powert = pygame.transform.rotate(font.render("POWER", True, (255,255,255)),90)
	anglet = font.render("ANGLE", True, (255,255,255))
	bg = pygame.image.load("data/images/lsdbowling/alley.png").convert()
	#pinx and pinz are the positions of the pins on the alley floor. 
	#May need some adjustment if you fool with the perspective code to keep them in the right place.
	pinx=[-64,-32,0,32,-48,-16,32,-32,0,-16]
	pinz=[900,900,900,900,868,868,868,836,836,804]
	pins=[]
	for i in range (10):
		newpin = pin(pinx[i], pinz[i])
		pins.append(newpin)
	you = ball()
	time = 0
	score = 0
	throw = 0
	power = 0
	powerup = 1
	angle = 0.0
	angleup = 1
	arewesettingup = 1
	acidx = 400
	acidy = 300
	acids = 1
	adx = random.randint(-16,16)
	ady = random.randint(-16,16)
	while (throw < 2):
		#Throws two balls for one frame total. No handling for a strike implemented at the moment. Good luck getting one anyway.
		if (arewesettingup == 1):
			dx, dy = pygame.mouse.get_rel()
			you.setup(dx, -dy)
			if (angleup == 1):
				angle += 0.1
			else:
				angle -= 0.1
			if (angle >= 3.0):
				angleup = 0
			if (angle <= -3.0):
				angleup = 1
			if (powerup == 1):
				power += 1
			else:
				power -= 1
			if (power >= 10):
				power = 10
				powerup = 0
			if (power <= 1):
				power = 1
				powerup = 1
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					arewesettingup = 0
				if event.type == KEYDOWN:
					raise SystemExit

		else:
			you.bowl(power,angle)
			for i in pins:
				if collision(i, you) == 1 and i.set == 1:
					i.fall(time)
					power -= 1
				if i.set == 0:
					i.fall(time)
			if you.z > 900 or power <= 0:
				for i in pins:
					if i.set == 0:
						score += 1
				arewesettingup = 1
				throw += 1
				you.reset()

		time += 1 #This might be a good place to put a call to pygame.time.something instead.
		screen.blit(bg, (0,0))
		for i in pins:
			i.show(screen)
		you.show(screen)
		powerpic=pygame.draw.rect(screen, (0,0,160),(32,0,16,power*5))
		anglepic=pygame.draw.rect(screen, (160,0,0),(40,50,10*angle,16))
		screen.blit(powert,(32,0))
		screen.blit(anglet,(10,50))
		#acidangle = random.randint(-1,1)
		#acidscale = 1 + random.random()/4
		#---------------BEGIN TRIPPINESS HERE------------------#
		if random.randint(0,9) == 1:
			adx = random.randint(-128,128)
			ady = random.randint(-128,128)
			if acids < 8:
				acids += 1
			elif acids > 1:
				acids -= 1
		acidx += adx
		acidy += ady
		if acidx < 0:
			adx *= -1
			acidx = 0
		if acidx > 800:
			adx *= -1
			acidx = 800
		if acidy < 0:
			ady *= -1
			acidy = 0
		if acidy > 600:
			ady *= -1
			acidy = 600
		acidrect = pygame.Rect(acidx,acidy,acids,acids)
		acid = pygame.transform.chop(screen,acidrect)
		for i in range(1,acids):
			acid = pygame.transform.rotate(acid, (-1**i))
		acid = pygame.transform.rotate(acid, acids-1)
		screen.blit(acid,(-9 * acids,-9 * acids))
		#---------------END TRIPPINESS HERE------------------#
		pygame.display.flip()
	return score #Note that this isn't a true bowling scoring system. Pins knocked down from the first ball are worth 2 points, second ball 1 point.

print main()
