// Standard stuff...
#include <iostream>
#include <cstdlib>
using namespace std;

// A class that represents a Monitor
//#define DEBUG
#include "Monitor.h"
#include "Monitor.cpp"

// OpenCV stuff...

int main(int argc, char const *argv[]) {
	vector<Monitor> supportedMonitors = Monitor::getSupportedMonitors();
	Monitor myMonitor = supportedMonitors.at(0);
	if (!myMonitor.canChangeBacklight()) {
		cout << "Run with sudo" << endl;
		return 1;
	}
	cout << (myMonitor.setBacklight(atof(argv[1])) ? "Setting value OK" : "Error setting value") << endl;
	return 0;
}
