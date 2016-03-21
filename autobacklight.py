#! /usr/bin/python2

from subprocess import call
import sys
import cv2
import time

# Constants that adjust the relation between the ambient light level and the backlight level
# Should be modified until the user get comfortable with the backlight and the changes
#
# You can think about these constants like the angular coeficient (slope) and the linear coeficient of a straight line equation
# BackLight = AmbLight*GAIN + BASE_LINE
GAIN = 1.0
BASE_LINE = 0.0

# Set the maximum number of steps from the minimum to the maximum value
# It's useful to avoid little changes constantly
# TODO
MAX_STEPS = 10

def main(argv):

	# It tests if the backlight sys_path is passed, otherwise the Xorg xbacklight will be used
	if (len(argv)>=2):
		SYS_PATH = argv[1]
		MAX_VALUE = int(open(SYS_PATH+"max_brightness", 'r').read())
		BRIGHTNESS_FILE = open(SYS_PATH+"brightness", 'w')
		while True:
			ambLight = getAmbientLightLevel()
			backLight = int(ambLight*GAIN*MAX_VALUE/100 + BASE_LINE)
			if (backLight < 0): backLight = 0
			BRIGHTNESS_FILE.write(str(backLight))
			BRIGHTNESS_FILE.flush()

			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")

			time.sleep(1)

	else:
		while True:
			ambLight = getAmbientLightLevel()
			backLight = int(ambLight*GAIN + BASE_LINE)
			#Set the screen backlight level whith the command "xbacklight" privided by Xorg.
			call(["xbacklight", "-set", str(backLight)])

			#Debug
			print("AmbLight:\t"+str(ambLight)+"\nBackLight:\t"+str(backLight)+"\n")

			time.sleep(1)

def getAmbientLightLevel():

	# Get the camera at location 0
	cap = cv2.VideoCapture(0)

	returnStatus, image = cap.read()

	# Get the height and the width (in pixels) of the image
	height = len(image)
	width = len(image[0])

	# Variable that will store the light intensity, calculated from the image pixels
	lightIntensity = 0

	# Get the central row of the image, which will be analyzed
	# Experimentally, I concluded that one row is sufficient to estimate the light intensity. Analysing the whole image is a waste of CPU power.
	centralRow = image[height/2]
	for pixel in centralRow:
		#In the HSV color space, the Intensity of a color (or a pixel), is giving by the max RGB value.
		#https://en.wikipedia.org/wiki/HSL_and_HSV
		lightIntensity += max(pixel)

	#Normalize the value to a scale of one pixel (0-255)
	lightIntensity /= width

	#Normalize the valur to a scale of 0-100
	lightIntensity /= 2.55

	return  lightIntensity

if __name__ == '__main__':
	main(sys.argv)