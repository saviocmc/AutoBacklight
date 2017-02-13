#! /usr/bin/python2
from subprocess import call
import sys
import cv2
import time

# Indicates the directory in your system where are the files that actually controls the backlight.
# Usually, it is "/sys/class/backlight/something"
# The directory must have the files "brightness" and "max_brightness" inside it.
#
# This variable is optional if the command 'xbacklight' (by Xorg) works in your computer
SYS_PATH = ""

# Constants that adjust the relation between the ambient light level and the backlight level
# Should be modified until you get comfortable with the backlight changes
#
# You can think about these constants like the angular coefficient (slope) and the linear coeficient of a straight line equation
# BackLight = AmbLight*GAIN + BASE_LINE (the AmbLight will be in a 0 to 1 scale)
GAIN = 1.0
BASE_LINE = 0.00

# The number of images captured per minute
# It is also the number of adjustments per minute that this app is gonna do
FREQUENCY = 60

# Set the maximum number of steps from the minimum to the maximum value of brightness
# It's useful to avoid constantly little changes
MAX_STEPS = 10

def main(argv):

	# Creates a AmbientLightSensor with the default system camera (for laptops, it's Usually the built-in camera)
	sensor = AmbientLightSensor(cv2.VideoCapture(0))

	global SYS_PATH
	if (len(SYS_PATH) > 0): # It's gonna use the system file 'brightness' under SYS_PATH to control the backlight
		if(not SYS_PATH.endswith("/")): SYS_PATH += "/"
		MAX_VALUE = int(open(SYS_PATH + "max_brightness", 'r').read())
		BRIGHTNESS_FILE = open(SYS_PATH + "brightness", 'w')

		global MAX_STEPS
		if (MAX_STEPS > MAX_VALUE): MAX_STEPS = MAX_VALUE

		print("\nThe MAX VALUE is "+str(MAX_VALUE)+"\n")

		while True:
			ambLight = sensor.getAmbientLightLevel()
			backLight = int(round(round((ambLight*GAIN + BASE_LINE)*MAX_STEPS)*(MAX_VALUE/MAX_STEPS)))
			if (backLight < 0): backLight = 0
			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")
			BRIGHTNESS_FILE.write(str(backLight))
			BRIGHTNESS_FILE.flush()
			time.sleep(60/FREQUENCY)

	else: # It's gonna use the command "xbacklight" privided by Xorg
		MAX_VALUE = 100
		print("\nThe MAX VALUE is 100\n")
		while True:
			ambLight = sensor.getAmbientLightLevel()
			backLight = round((ambLight*GAIN + BASE_LINE)*MAX_STEPS)*(MAX_VALUE/MAX_STEPS)
			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")
			call(["xbacklight", "-set", str(backLight)])
			time.sleep(60/FREQUENCY)

class AmbientLightSensor(object):
	"""
		This class uses a camera (usually a web-cam) to detect and provide the level of luminosity in the ambient
		It uses the camera to take pictures and analyzes the intensity of it's pixels
	"""
	def __init__(self, camera):
		super(AmbientLightSensor, self).__init__()
		self.camera = camera
		self.image_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.image_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

	def getAmbientLightLevel(self):
		"""	Returns the luminosity level in the ambient in a scale of 0 to 1	"""

		# TODO Need to find a way around it
		# This, for now, is needed to avoid the built-in auto-adjustment of brightness of the camera
		# One possible way is to disable the auto-adjustment via 'v4l2ctrl' command (or it's graphical equivalent v4l2ucp)
		# The problem with this is, for some reason, there is a delay between the ambient light change and it's detection
		self.camera.release()
		self.camera = cv2.VideoCapture(0)

		# Take a picture and store it in 'image' variable
		returnStatus, image = self.camera.read()

		# Variable that will store the light intensity, calculated from the image pixels
		lightIntensity = 0

		# Get the central row of the image, which will be analyzed
		# Experimentally, I concluded that one row is sufficient to estimate the light intensity. Analysing the whole image is a waste of CPU power.
		centralRow = image[self.image_height/2]
		for pixel in centralRow:
			# In the HSV color space, the Intensity of a color (or a pixel), is giving by the max RGB value.
			# https://en.wikipedia.org/wiki/HSL_and_HSV
			lightIntensity += max(pixel)

		# Normalize the value to a scale of one pixel (0 to 255)
		lightIntensity /= self.image_width

		# Normalize the value to a scale of 0 to 1
		lightIntensity /= 255

		return  lightIntensity

if __name__ == '__main__':
	main(sys.argv)
