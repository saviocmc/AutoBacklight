#include "Monitor.h"
#include <fstream>
#include <cmath>
#include <boost/filesystem.hpp>
namespace fs = boost::filesystem;

vector<Monitor> Monitor::getSupportedMonitors(string baseSysPath) {
    vector<Monitor>* monitors = new vector<Monitor>;
    for (fs::directory_entry& entry : fs::directory_iterator(baseSysPath)){
        string monitorPath = entry.path().string() + '/';
        if (
            fs::is_directory(entry) &&
            fs::is_regular_file(monitorPath + "brightness") &&
            fs::is_regular_file(monitorPath + "max_brightness") &&
            fs::is_regular_file(monitorPath + "actual_brightness")
        )
        monitors->push_back(*(new Monitor(monitorPath)));
    }
    return *monitors;
}

Monitor::Monitor(string pathToBacklightSysDir) {

    _sysPath = pathToBacklightSysDir;
    if (_sysPath.back() != '/') _sysPath.push_back('/');
    //get the max_brightness value in it's reference file
    fstream(_sysPath + "max_brightness", ios::in) >> _max_brightness;
    _margin_of_error = (double)1/(_max_brightness*2);
    //get the actual_brightness value in it's reference file
    fstream(_sysPath + "actual_brightness", ios::in) >> _actual_brightness;

    #ifdef DEBUG
    cout << endl;
    cout << "Monitor sysPath:   " << _sysPath << endl;
    cout << "max_brightness:    " << _max_brightness << endl;
    cout << "actual_brightness: " << _actual_brightness << endl;
    cout << "margin_of_error:   " << _margin_of_error << endl;
    cout << endl;
    #endif
}

double Monitor::getBacklight() {
    fstream(_sysPath + "actual_brightness", ios::in) >> _actual_brightness;
    return (double)_actual_brightness/(double)_max_brightness;
}

bool Monitor::setBacklight(double backlight) {
    fstream(_sysPath + "brightness", ios::out) << round(backlight*_max_brightness);
    return abs(backlight - getBacklight()) <= _margin_of_error;
}

bool Monitor::increaseBacklight(double increment) {
    if (abs(increment) > _margin_of_error) {
        return setBacklight(getBacklight() + increment);
    } else {
        #ifdef DEBUG
        cout << "ERROR: The minimum value of increment or decrement to make any difference is" << _margin_of_error << endl;
        cout << "Value passed was " << increment << endl << endl;
        #endif
        return false;
    }
}

bool Monitor::decreaseBacklight(double decrement) {
    return increaseBacklight(-decrement);
}

bool Monitor::canChangeBacklight() {
    return !(!fstream(_sysPath + "brightness", ios::out));
}
