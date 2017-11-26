"""
tabletop is a linux-python tool which disables the keyboard(s) on a laptop
so that the laptop keyboard surface can be used comfortably as a work table.

Developer: Chan Jun Shern (chanjunshern@gmail.com)
"""
import sys
from select import select
from evdev import InputDevice, list_devices, ecodes

def quit_tabletop():
    """
    Exit program gracefully
    """
    for _fd in devices:
        try:
            devices[_fd].ungrab()
        except IOError:
            print "Already ungrabbed."
    print "Thank you for using tabletop!"
    print " "
    sys.exit()
    return

def main():
    """
    Main function
    """
    print "_____TABLETOP V1.0_____\nWelcome to tabletop!\n"

    ## Detect keyboards
    devices_list = list()
    for dev in list_devices():
        input_dev = InputDevice(dev)
        rate = input_dev.repeat[0] # Extract keyboard repeat rate
        if rate > 0: ## Will be zero unless it's a keyboard! :)
            devices_list.append(input_dev.fn)
    devices = map(InputDevice, devices_list)
    devices = {dev.fd: dev for dev in devices}
    num_devices = len(devices)
    print num_devices, "keyboard(s) detected."
    if num_devices == 0:
        print "Please ensure that you are root, and that you have keyboards connected."
        print " "
        quit_tabletop()


    # Grab keyboards
    for _fd in devices.keys():
        try:
            devices[_fd].grab()
            print "Disabled keyboard", devices[_fd].name
        except IOError:
            print "Already grabbed."
    print "(Press ESC to quit)"

    ## Main loop
    quitting_state = False
    while True:
        rlist, _, _ = select(devices, [], [])
        for filedevice in rlist:
            for event in devices[filedevice].read():
                # Identify key
                keyname = ecodes.KEY[event.code]
                if event.type == ecodes.EV_KEY:
                    ## KEYDOWN
                    if event.value == 1:
                        if quitting_state:
                            if keyname == "KEY_ENTER":
                                quit_tabletop()
                            else:
                                quitting_state = False
                                print "Resuming tabletop"
                        elif keyname == "KEY_ESC":
                            quitting_state = True
                            print "\nESC pressed, are you sure you want to quit? (ENTER)"

devices = {}
main()
