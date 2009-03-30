import pickle

#This script simply reads in .pbm images as level data for each object in Super Platform Jump. A black pixel stands for an object of each type.
#There should be an image file for each object type.
#The resulting data is stored in a pickle file.
#You probably don't want to mess with this code, but it could easily be converted to handle more object types for a better game.
#For designing your own levels, be sure to save the .pbm files as ASCII.

class proto():
	def __init__(self, x, y):
		self.x = x
		self.y = y

def main():
	objects = ["ground", "rock", "brick", "coin"]
	for i in objects:
		world = []
		f = open("project/gimp/spj" + i + ".pbm", 'r')
		#These two readlines are just to throw away the header lines in the .pbm files.
		f.readline()
		f.readline()
		#Reads in the scale of the image and unpacks the string into two ints.
		scale = f.readline()
		xmax, sep, ymax = scale.partition(' ')
		xmax = int(xmax)
		ymax = int(ymax)
		#And this is the important loop that actually reads each pixel. In .pbm files, a 1 is black and 0 is white. We're only worried about the 1's.
		s = f.read(1)
		for y in range(ymax):
			for x in range(xmax):
				repeat = 1
				while repeat == 1:
					if s == '1':
						newobst = proto(x*64,y*64-536)
						world.append(newobst)
						repeat = 0
					elif s == '0':
						repeat = 0
					else:
						repeat = 1
					s = f.read(1)
		f.close()
		f = open("data/map/superplatformjump/spj" + i + ".lev", 'w')
		pickle.dump(world, f)
		f.close()

main()


