#########################################################################################
#	Uplotopia V0.1                                                                  #
#	by Callonz                                                                      #
#	Tested with python 2.7, but will probaby work with other versions also.         #
#########################################################################################
import requests, pyperclip, sys, pygame, os, datetime, time, subprocess
from playsound import playsound
from PIL import Image
import pyscreenshot as ImageGrab

##############################################################################################################
#	Config
url = "https://example.com"
passwd = "123456"
# This is where the image will be saved locally
folderpath = "/home/user/Pictures"
# This will result in filenames looking like this: YYY-MM-DD_hh_mm_ss
filename_format = str(datetime.datetime.now()).split('.')[0].replace(':','_').replace(' ', '_')
filename = folderpath + filename_format + '.png'
filename_area = folderpath + filename_format + '_area.png'
upload_text = folderpath + filename_format + ".txt"
#	Config End - You won't need to edit anything past this point
##############################################################################################################

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
	
def Area():
	tmp = ImageGrab.grab()
	tmp.save(filename)
	input_loc = filename		
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
		im.save(filename_area)
	else:
		im = Image.open(input_loc)
		im = im.crop(( left, upper, right, lower))
		pygame.display.quit()
		im.save(filename_area)
#-#

def Fullscreen():
	im = ImageGrab.grab()
	im.save(filename)

def Text():
	try:
		# for Python2
		from Tkinter import * 
	except ImportError:
		# for Python3
		from tkinter import * 
	r = Tkinter.Tk()
	txt = r.clipboard_get()
	if len(txt.get()) == 0:
		#There is no text in clipboard, exiting
		sys.exit("Clipboard is empty.")
	text_file = open(upload_text, "w")
	text_file.write(txt)
	text_file.close()
		
if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "fullscreen":
			# grab fullscreen
			type = 0
			Fullscreen()
		elif sys.argv[1] == "area":
			#im = ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
			type = 1		
			Area()
		elif sys.argv[1] == "text":
			type = 2
			Text()
	else:
		#defaulting to fullscreen
		type = 0
		Fullscreen()

			
userdata = {"k": passwd}

if type == 0:
	uploadfile = filename
	showprev = 1	
if type == 1:
	uploadfile = filename_area
	showprev = 1
if type == 2:
	uploadfile = upload_text
	showprev = 0

file = {'d': open(uploadfile, 'rb')}
resp = requests.post(url, data=userdata, files=file)
responsetext = str(resp.text)
pyperclip.copy(responsetext)
showPreview(uploadfile)
if showprev == 1:	
	showPreview(uploadfile)
# this needs fixing lel
#playsound(os.getcwd() + '/success.wav')
