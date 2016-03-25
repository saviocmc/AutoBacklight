# Auto Backlight

This is a Python2 application that sets the screen backlight (brightness) according to the ambient light. It uses a camera (usually a web-cam) to detect the level of luminosity in the ambient and calculates and sets the appropriate backlight value.

## Config Variables

Following the Python way of codding, the app code is self explanatory and well documented. To adjust it's behavior to fit your preferences, you must modify some constants in the beginning of the code.

###### SYS_PATH
Is the directory that holds the files `brightness` and `max_brightness`. The file brightness is the one that actually controls the backlight level. It is usually `/sys/class/backlight/something`.
This variable is optional if the command 'xbacklight' (by Xorg) works in your computer.

###### GAIN and BASE_LINE
Constants that adjust the relation between the ambient light level and the backlight level
Should be modified until you get comfortable with the backlight changes.

You can think about these constants like the angular coefficient (slope) and the linear coeficient of a straight line equation
`BackLight = AmbLight*GAIN + BASE_LINE` (the AmbLight will be in a 0 to 1 scale).

###### FREQUENCY
The number of images captured and adjustments per minute that this app is gonna do. I recommend `60` (1 adjustment per second).

###### MAX_STEPS
Set the maximum number of steps from the minimum to the maximum value of brightness. It's useful to avoid constantly little changes. I think `10` is a good number for that.
