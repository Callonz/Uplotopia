#########################################################################################
#	Uplotopia V0.2                                                                  #
#	by Callonz                                                                      #
#	Tested with python 2.7, but will probaby work with other versions also.         #
#########################################################################################
import requests, pyperclip, sys, datetime, pygame, os, time, subprocess, configparser
from playsound import playsound
from PIL import Image
import pyscreenshot as ImageGrab

config = configparser.ConfigParser()
c_path, c_file = os.path.split(os.path.realpath(__file__))
config.read(c_path + '/config.ini')

# technically it would be possible to define multiple hosts and calling upon them via argv's and loading them accordingly in this part, but this has a very low priority for me so maybe I will add this sometime in the future
default = config['DEFAULT']

url = default['url']
passwd = default['key']
folderpath = default['folderpath']

def showPreview(path):
	# The following part is for getting the current screen resolution so I can display the preview. I know there are better way of doing this and I may change it in the future but for now this works	
	cmd = ['xrandr']
	cmd2 = ['grep', '*']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
	p.stdout.close()
	 
	resolution_string, junk = p2.communicate()
	resolution = resolution_string.split()[0]
	width, height = resolution.split('x')
	
	# Size of the preview window, might make it more dynamic in the future
	w = 300
	h = 150
	size=(w,h)

	# calculating the starting position of the preview window
	x = int(width) - w
	y = int(height) - h
	
	In=1
	
	# Setting the starting position for pygame
	os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(x,y)
	pygame.init()

	# defining the preview windows as screen
	screen = pygame.display.set_mode(size, pygame.NOFRAME) 
	c = pygame.time.Clock() # create a clock object for timing

	while True:
		if currentupload.type == 'png': #this results in the preview for a non-image upload just being black, this needs to be fixed later on
			px = pygame.image.load(path)
			px = pygame.transform.scale(px, (w, h))
			screen.blit(px, px.get_rect())
			pygame.display.flip()
			screen.blit(px,(0,0))
		pygame.display.flip() # update the display
		c.tick(3) # only three images per second
		In += 1
		if In == 5:	# end the preview after 5 iterations
			break

def config():
	# Size of the config window
	w = 500
	h = 500
	size=(w,h)


	In=1

	pygame.init()

	# defining the preview windows as screen
	screen = pygame.display.set_mode(size, pygame.NOFRAME) 
	c = pygame.time.Clock() # create a clock object for timing

	while True:
		#if currentupload.type == 'png': #this results in the preview for a non-image upload just being black, this needs to be fixed later on
		#	px = pygame.image.load(path)
		#	px = pygame.transform.scale(px, (w, h))
		#	screen.blit(px, px.get_rect())
		#	pygame.display.flip()
		#	screen.blit(px,(0,0))
		pygame.display.flip() # update the display
		c.tick(3) # only three images per second
		In += 1
		#if In == 5:	# end the preview after 5 iterations
		#	break	
		
# Thanks to samplebias for the following code (https://stackoverflow.com/questions/6136588/image-cropping-using-python/8696558)
#-#
def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)
def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n=0
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = event.pos
                else:
                    bottomright = event.pos
                    n=1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return ( topleft + bottomright )
	
def Area(currentupload):
	tmp = ImageGrab.grab()
	tmp.save(currentupload.getFilename())
	input_loc = currentupload.getFilename()		
	screen, px = setup(input_loc)
	left, upper, right, lower = mainLoop(screen, px)
	# ensure output rect always has positive width, height
	if right < left:
		left, right = right, left
	if lower < upper:
		lower, upper = upper, lower
		im = Image.open(input_loc)
		im = im.crop(( left, upper, right, lower))
		pygame.display.quit()
		im.save(currentupload.getFilename())
	else:
		im = Image.open(input_loc)
		im = im.crop(( left, upper, right, lower))
		pygame.display.quit()
		im.save(currentupload.getFilename())
#-#

class _UploadFile:
	
	def __init__(self, type):
		if type == 0:
			ext = '.png'
			self.type = 'png'
		if type == 1:
			ext = '_area.png'
			self.type = 'png'
		if type == 2:
			ext = '.txt'
			self.type = 'txt'

		date = str(datetime.datetime.now()).split(' ')[0]	
		time = str(datetime.datetime.now()).split(' ')[1].split('.')[0]
		year = date.split('-')[0]
		month = date.split('-')[1]
		day = date.split('-')[2]
		hour = time.split(':')[0]
		minute = time.split(':')[1]
		second = time.split(':')[2]
		filename = default['filename'].replace('&Y',year).replace('&M',month).replace('&D',day).replace('&h',hour).replace('&m',minute).replace('&s',second)
		filename = default['folderpath'] + filename + ext 	
		self.name = filename		

	def getFilename(self):
		return self.name

def Fullscreen(currentupload):
	im = ImageGrab.grab()
	im.save(currentupload.getFilename())

def Text(currentupload):
	try:
		# for Python2
		import Tkinter 
	except ImportError:
		# for Python3
		import tkinter 
	# Using tkinter to grab the clipboard text results in an empty tkinter windows showing up. This will be fixed later on as it doesn't bother me too much at the moment
	r = Tkinter.Tk()
	txt = r.clipboard_get()
	if len(txt) == 0:
		#There is no text in clipboard, exiting
		sys.exit("Clipboard is empty.")
	text_file = open(currentupload.getFilename(), "w")
	text_file.write(txt)
	text_file.close()
		

if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "fullscreen":
			# grab fullscreen
			currentupload = _UploadFile(0)
			Fullscreen(currentupload)
		elif sys.argv[1] == "area":
			# grab an area
			currentupload = _UploadFile(1)		
			Area(currentupload)
		elif sys.argv[1] == "text":
			# upload text in clipboard
			currentupload = _UploadFile(2)
			Text(currentupload)
		elif sys.argv[1] == "config":
			# initiate config
			config()
			sys.exit()
		else:
			# Unknown argv, exiting		
			sys.exit("Argument not defined.")

	else:
		#if no argv is given it will only play the success sound. this is so I can call the script itself later on after the upload as a subprocess, so that the preview and sound appear at the same time.  
		playsound(c_path + '/success.wav')
		sys.exit()


			
userdata = {"k": passwd}

uploadfile = currentupload.getFilename()


file = {'d': open(uploadfile, 'rb')}
resp = requests.post(url, data=userdata, files=file) 			# This is there the actual upload happens
responsetext = str(resp.text)									# grabbing the response from the server
subprocess.Popen([sys.executable, c_path + "/uplotopia.py"])	# starting a subprocess of calling this file again so it plays the "success.wav" sound 
pyperclip.copy(responsetext)									# copying the responsetext (most likely the link to the uploaded file) to the clipboard
showPreview(uploadfile)											# showing a preview of the image - if the file was not an image it's just a black screen for now
sys.exit()														# :)