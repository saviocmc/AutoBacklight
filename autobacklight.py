#! /usr/bin/python2
from subprocess import call
import sys
import cv2
import time

# Indicates the directory in your system where are the files that actually controls the backlight.
# Usualy, it is "/sys/class/backlight/something"
# The directory must have the files "brightness" and "max_brightness" inside it.
SYS_PATH = "/sys/class/backlight/acpi_video0"

# Constants that adjust the relation between the ambient light level and the backlight level
# Should be modified until the user get comfortable with the backlight and the changes
#
# You can think about these constants like the angular coeficient (slope) and the linear coeficient of a straight line equation
# BackLight = AmbLight*GAIN + BASE_LINE
GAIN = 1.0
BASE_LINE = 0.0

# The number of images captured per minute
# It is also the number of ajustmens per minute that the app is gonna do
FREQUENCY = 120

# Set the maximum number of steps from the minimum to the maximum value of brightness
# It's useful to avoid constantly little changes
# TODO
MAX_STEPS = 10

def main(argv):
	# First, it tests if the SYS_PATH is passed

	if (len(SYS_PATH) > 0): # Using the system file 'brightness' under SYS_PATH to control the backlight
		global SYS_PATH
		if(not SYS_PATH.endswith("/")): SYS_PATH += "/"
		MAX_VALUE = int(open(SYS_PATH + "max_brightness", 'r').read())
		BRIGHTNESS_FILE = open(SYS_PATH + "brightness", 'w')

		while True:
			ambLight = getAmbientLightLevel()
			backLight = int(ambLight*GAIN*MAX_VALUE/100 + BASE_LINE)
			if (backLight < 0): backLight = 0
			BRIGHTNESS_FILE.write(str(backLight))
			BRIGHTNESS_FILE.flush()
			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")
			time.sleep(60/FREQUENCY)

	else: # Using the command "xbacklight" privided by Xorg
		while True:
			ambLight = getAmbientLightLevel()
			backLight = int(ambLight*GAIN + BASE_LINE)
			call(["xbacklight", "-set", str(backLight)])
			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")
			time.sleep(60/FREQUENCY)

def getAmbientLightLevel():

	# Get the camera at location 0
	cam = cv2.VideoCapture(0)

	returnStatus, image = cam.read()

	# Get the height and the width (in pixels) of the image
	height = len(image)
	width = len(image[0])

	# Variable that will store the light intensity, calculated from the image pixels
	lightIntensity = 0

	# Get the central row of the image, which will be analyzed
	# Experimentally, I concluded that one row is sufficient to estimate the light intensity. Analysing the whole image is a waste of CPU power.
	centralRow = image[height/2]
	for pixel in centralRow:
		# In the HSV color space, the Intensity of a color (or a pixel), is giving by the max RGB value.
		# https://en.wikipedia.org/wiki/HSL_and_HSV
		lightIntensity += max(pixel)

	# Normalize the value to a scale of one pixel (0-255)
	lightIntensity /= width

	# Normalize the value to a scale of 0-100
	lightIntensity /= 2.55

	return  lightIntensity

if __name__ == '__main__':
	main(sys.argv)
