import pygame, math, pickle, random
from pygame.locals import *

#These constants are just to make it easier to read states and stuff. Their values are arbitrary. IDLE, WALKING, and JUMPING should all be different from each other.
#TOP, BOT, LEFT, and RIGHT should all be different from each other.
IDLE = 0
WALKING =1
JUMPING =2
TOP = 0
BOT = 1
LEFT = 2
RIGHT = 3 

class player(): 
	def __init__(self, x, y): 
		self.x = x 
		self.y = y 
		self.xvel = 0
		self.yvel = 0
		self.score = 0
		self.state = IDLE
		self.facing = 1
		self.grounded = 0
		self.startjump = 1
		self.canjump = 1
		self.jumpbuttonup = 1
		self.cframe = 0
		self.walkcount = 0
		self.frame = []
		for i in range(1,5):
			newframe = pygame.image.load("data/images/superplatformjump/guy" + str(i) + ".png").convert_alpha()
			self.frame.append(newframe)

	def collision(self, obst):
		#Here's a decent example of pygame's built-in collision detection for all you noobs.
		srect = pygame.rect.Rect(self.x, self.y, 64, 128).inflate(-2,-2)
		orect = pygame.rect.Rect(obst.x, obst.y, 64, 64).inflate(-2,-2)
		if srect.colliderect(orect):
			return 1
		else:
			return 0

	def collision_angle(self, obst):
		#And here's an uglier block of junk to see what side of the rect that collision came from. It's faster than it looks.
		sleft = self.x
		sright = self.x + 64
		stop = self.y
		sbot = self.y + 128
		oleft = obst.x
		oright = obst.x + 64
		otop = obst.y
		obot = obst.y + 64
		if sbot < obot:
			return BOT
		if stop > otop:
			return TOP
		if sleft > oleft:
			return LEFT 
		if sright < oright:
			return RIGHT


	def idle(self):
		#This isn't perfect and results in some bouncing, but what it does is keep gravity working if the guy isn't doing anything.
		self.startjump = 1
		if self.xvel < 0:
			self.xvel += 1
		if self.xvel > 0:
			self.xvel -= 1
		if self.yvel < 8:
			self.yvel += 1

	def walk(self):
		self.startjump = 1
		self.xvel += self.facing
		if abs(self.xvel) > 8:
			self.xvel -= self.facing
		if self.yvel < 8:
			self.yvel += 1
		self.walkcount += 1
		if self.walkcount > 12: #Change this value if you fool with the animation block down in update() and need a higher or lower amount of game frames for
					#the walk cycle loop.
			self.walkcount = 0

	def jump(self):
		#I hate writing jump functions. Tried to make this one quick and painless and handle most of it in the game physics.
		if self.startjump == 1:
			self.yvel = -16
			self.startjump = 0
		else:
			if self.yvel < 8:
				self.yvel += 1
				if self.yvel >= 0:
					self.canjump = 0

	def take_input(self, left, right, jump):
		#This doesn't actually read input from anywhere. It takes the states of three pretend buttons as values. You could attach an a.i. to this or whatever.
		if jump == 1 and self.canjump == 1:
			self.state = JUMPING
			self.jumpbuttonup = 0
			if left == 1 or right == 1:
				if abs(self.xvel) < 4:
					self.xvel += self.facing
		elif left == 1:
			self.facing = -1
			if self.grounded == 1:
				self.state = WALKING
			else:
				self.x += self.facing
		elif right == 1:
			self.facing = 1
			if self.grounded == 1:
				self.state = WALKING
			else:
				self.x += self.facing
		else:
			self.state = IDLE
		if jump == 0:
			self.jumpbuttonup = 1

	def update(self, world, coins, cam):
		self.x += self.xvel
		self.y += self.yvel
		self.grounded = 0
		for i in world:
			if cam.rect().colliderect(i.rect()):
				#Only update an object if it's on screen. Doesn't seem to affect the speed as much as in other games though. Not sure why.
				if self.collision(i) == 1:
					collision_vector = self.collision_angle(i)
					if self.yvel > 0:
						if collision_vector==BOT:
							self.grounded = 1
							self.y = i.y - 129
							self.yvel = 0
							if self.jumpbuttonup == 1:
								self.canjump = 1
					elif self.yvel < 0:
						if collision_vector==TOP:
							self.y = i.y + 65
							self.yvel = 0
					if self.xvel > 0:
						if collision_vector==RIGHT:
							self.x = i.x - 65
							self.xvel = 0
					elif self.xvel < 0:
						if collision_vector==LEFT:
							self.x = i.x + 65
							self.xvel = 0

		for i in coins:
			if cam.rect().colliderect(i.rect()):
				if self.collision(i) == 1:
					self.score += 1
					coins.remove(i)



		if self.state == WALKING:
			self.walk()
		if self.state == JUMPING:
			self.jump()
		if self.state == IDLE:
			self.idle()



		if self.state == IDLE:
			self.cframe = 0
		elif self.state == WALKING:
			#If you want better animation, you can pretty much fool with this arbitrarily. Determines what frame of the guy to show while walking.
			#If you want a different maximum for walkcount, change it in the walk function.
			if self.walkcount < 3:
				self.cframe = 1
			elif self.walkcount < 6:
				self.cframe = 0
			elif self.walkcount < 9:
				self.cframe = 3
			else:
				self.cframe = 0
		elif self.state == JUMPING:
			self.cframe = 2

	def show(self, screen, cam):
		cam.move(self.x - 400, self.y - 64 )
		if self.facing == 1:
			screen.blit(self.frame[self.cframe], (self.x-cam.x, self.y-cam.y))
		elif self.facing == -1:
			screen.blit(pygame.transform.flip(self.frame[self.cframe],True,False), (self.x-cam.x, self.y-cam.y))
			

#If you wanna add bad guys or npcs to yours, this would be the place to write classes for them. You could derive them from player() or write them from scratch.
#If you derive them from player, you probably want to overload any function that changes anything in cam, namely the show() function.

class obstacle():
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
	def rect(self):
		return pygame.rect.Rect(self.x, self.y, 64, 64)

	def show(self, screen, cam):
		screen.blit(self.sprite,(self.x-cam.x,self.y-cam.y))

class coin():
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
	def rect(self):
		return pygame.rect.Rect(self.x, self.y, 64, 64)


	def show(self, screen, cam):
		screen.blit(self.sprite,(self.x-cam.x,self.y-cam.y))


class camera():
	def __init__(self):
		self.x = 0
		self.y = 0
	def move(self, x, y):
		self.x = x
		self.y = y
		if self.x < 0:
			self.x = 0
		if self.y > 0:
			self.y = 0
	def rect(self):
		return pygame.rect.Rect(self.x, self.y, 800, 600)

class proto():
	def __init__(self,x,y):
		self.x = x 
		self.y = y

def main():
	pygame.init()
	random.seed()
	screen = pygame.display.set_mode((800,600),FULLSCREEN)
	pygame.mouse.set_visible(False)
	font = pygame.font.SysFont("Terminal", 28, True)
	annoy = pygame.image.load("data/images/superplatformjump/annoy.png").convert()
	showannoy = 0
	you = player(200, 200) 
	dead = 0
	world = []
	tiletypes = ["ground", "rock", "brick"]
	for j in tiletypes:
		#The .lev files referenced here are produced with spjlc.py. Check its code for details.
		f = open("data/map/superplatformjump/spj" + j + ".lev", 'r')
		tiles = pickle.load(f)
		f.close()
		for i in tiles:
			newobst = obstacle(i.x, i.y, pygame.image.load("data/images/superplatformjump/" + j + ".png").convert())
			world.append(newobst)
	coins = []
	f = open("data/map/superplatformjump/spjcoin.lev", 'r')
	coinprotos = pickle.load(f)
	f.close()
	for j in coinprotos:
		newcoin = coin(j.x, j.y, pygame.image.load("data/images/superplatformjump/coin.png").convert_alpha())
		coins.append(newcoin)
	cam = camera()
	time = 3000
	while dead == 0:
		#----This is how you read keys action-style. If the key is down in this frame, it gets read. So the player doesn't have to keep tapping them.----#
		pygame.event.pump()
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			left = 1
		else:
			left = 0
		if keys[K_RIGHT]:
			right = 1
		else:
			right = 0
		if keys[K_z]:
			jump = 1
		else:
			jump = 0
		if keys[K_q]:
			print you.score
			raise SystemExit
		#----END ACTION-STYLE KEY READING CODE----#
		you.take_input(left,right,jump)
		you.update(world, coins, cam) 
		if you.y > 600: 
			dead = 1
		#---I JUST PUT THIS HERE TO IRRITATE PLAYERS FOR DRINKING PURPOSES. TAKE IT OUT FOR A REAL PLATFORMER.---#
		if random.randint(0,500)==50:
			showannoy = 1
		if random.randint(0,30) == 15:
			showannoy = 0
		#---END IRRITATING CODE---#
		pygame.draw.rect(screen,(64,160,255),(0,0,800,600)) 
		for i in world: 
			if cam.rect().colliderect(i.rect()):
				i.show(screen, cam)
		for i in coins:
			if cam.rect().colliderect(i.rect()):
				i.show(screen, cam)
		you.show(screen, cam)
		timeleft = font.render("TIME: " + str(time/10.0),True,(255,255,255))
		coinsleft = font.render("COINS LEFT: " + str(20-you.score),True,(255,255,255))
		screen.blit(timeleft,(0,0))
		screen.blit(coinsleft,(400,0))
		if showannoy == 1:
			screen.blit(annoy, (0,0))
		pygame.display.flip()
		time -= 1
		if time <= 0:
			dead = 1
	return you.score
print main()
