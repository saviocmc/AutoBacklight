# Auto Backlight

This is a Python2 application that sets the screen backlight (brightness) according to the ambient light. It uses a camera (usually a web-cam) to detect the level of luminosity in the ambient and calculates and sets the appropriate backlight value.

## Config Variables

Following the Python way of coding, the app code is mostly self explanatory and well documented. To adjust it's behavior to fit your preferences, you must modify some constants in the beginning of the code.

##### SYS_PATH
Is the directory that holds the files `brightness` and `max_brightness`. The file brightness is the one that actually controls the backlight level. It is usually `/sys/class/backlight/something`.
This variable is optional if the command 'xbacklight' (by Xorg) works in your computer.

##### GAIN and BASE_LINE
Constants that adjust the relation between the ambient light level and the backlight level
Should be modified until you get comfortable with the backlight changes.

You can think about these constants like the angular coefficient (slope) and the linear coeficient of a straight line equation
`BackLight = AmbLight*GAIN + BASE_LINE` (the AmbLight will be in a 0 to 1 scale).

##### FREQUENCY
The number of images captured and adjustments per minute that this app is gonna do. I recommend `60` (1 adjustment per second).

##### MAX_STEPS
Set the maximum number of steps from the minimum to the maximum value of brightness. It's useful to avoid constantly little changes. I think `10` is a good number for that.

# How to Install it

First, you must have the Python library *opencv*. In ArchLinux, just install this package: `sudo pacman -S opencv`. In Ubuntu, you can type `sudo apt-get install python-opencv`.

Now, you can [download the zip](https://github.com/saviocmc/AutoBacklight/archive/master.zip) containing the files and extract it to someplace in you computer.

If you have the *xbacklight* command working in your computer, great! To test, just type `xbacklight -set 0`. The backlight should go down to it's minimum value. Typing `xbacklight -set 100`, should set the maximum value. If the `xbacklight` doesn't work, you have to specify the SYS_PATH variable in the autobacklight.py and also run it with `sudo`.

With that said, open a terminal and go to the place you extracted the files. You can type `python2 autobacklight.py` or `sudo python2 autobacklight.py` (if you had set a SYS_PATH). The app should be running by now.

You will see two lines being constantly printed, containing the ambient light level read from the camera and the correspondent backlight that is been set. To stop it, press `ctrl+c`. Now is the time to modify the other variables in the file autobacklight.py and test the results.

Once you have set the variables for your preferences and the app is working fine, you can do the following in order to auto start it on login:

```
cp autobacklight.desktop ~/.config/autostart
sudo mkdir /opt/autobacklight
sudo cp autobacklight.py /opt/autobacklight/autobacklight.py
```

This should work fine if you are using *xbacklight*.

If you are not, theres no a good way to make it start at login. One solution is to change the Exec line of autobacklight.desktop to `sudo /opt/autobacklight/autobacklight.py &`, then make the file executable with `sudo chmod +x /opt/autobacklight/autobacklight.py` and finaly add the line `USERNAME ALL = NOPASSWD: /opt/autobacklight/autobacklight.py` to the */etc/sudoers* file (use `sudo visudo` for that). Replace USERNAME by you user name.

It works, but I do not recommend messing up with your */etc/sudoers* file unless you know what you're doing.

Sooner I'm gonna create the *systemd* service files, which will resolve this issue.
