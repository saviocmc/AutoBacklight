#ifndef MONITOR_H
#define MONITOR_H

#include <iostream>
#include <vector>

using namespace std;

// Represents a monitor and has methods for controlling the backlight
class Monitor {

public:

	// @param pathToBacklightSysDir indicates the directore in the system where
	// are the files to control the backlight of the mnitor
	// It is usally "/sys/class/backlight/something"
	Monitor(string pathToBacklightSysDir);

	// Returns the actual value of the backlight, in a 0 to 1 scale.
	double getBacklight();

	// Sets the value of the backlight, in a 0 to 1 scale.
	bool setBacklight(double backlight);

	// Increments the value of the backlight by "increment", in a 0 to 1 scale.
	bool increaseBacklight(double increment);

	// Decrements the value of the backlight by "decrement", in a 0 to 1 scale.
	bool decreaseBacklight(double decrement);

	// Returns true if the the program has permition to write to the
	// ACPI interface files. Returns false otherwise. Usually is necessary
	// to have root privileges to write to the files.
	bool canChangeBacklight();

	// Returns a vector with all the Monitor that can have they backlight
	// controlled by this program (with the Linux ACPI interface)
	static vector<Monitor> getSupportedMonitors(string baseSysPath = "/sys/class/backlight/");

private:
	string _sysPath;
	uint64_t _actual_brightness;
	uint64_t _max_brightness;
	double _margin_of_error;
};

#endif
