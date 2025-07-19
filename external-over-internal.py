"""Script to grab laptop-keyboard eventss from kernel, so I can have
external keyboard ontop of my laptop keyboard without meyhem.

https://python-evdev.readthedocs.io/en/latest/tutorial.html

https://www.freedesktop.org/software/libevdev/doc/latest/group__init.html#ga5d434af74fee20f273db568e2cbbd13f
This is what I do in c
"""

import evdev
import time

def find_external(devices, externals):
    for device in devices:
        for external in externals:
            if external == device.name:
                print(f"Found external keyboard path: {device.path}")
                return device.path
    return ""

"""Find device path with name that matches input"""
def find_internal(devices, internal):
    for device in devices:
        if internal == device.name:
            print(f"Found internal keyboard path: {device.path}")
            return device.path
    return ""


def get_info(dev_path='/dev/input/event6'):
    "Some debug info about device in path"
    dev = evdev.InputDevice(dev_path)
    print(f"\n {dev}\n")
    print(dev.capabilities(verbose=True))

    print("Check LED state")
    print(dev.leds(verbose=True))

    print("Check active keys")
    print(dev.active_keys(verbose=True))


# todo https://python-evdev.readthedocs.io/en/latest/apidoc.html
def getKey(dev):
    "dev - input device"
    # https://raspberrypi.stackexchange.com/questions/50007/mapping-key-events-using-evdev
    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            c = evdev.categorize(event)
            if c.keystate == c.key_down:
                yield c.keycode


if __name__ == "__main__":
    # Identified & copied from reading output of all devices:
    laptop_keyboard_name = "Asus Keyboard"
    external_keyboard_names = ["RK-KB3.0", "RK-KB5.0", "Compx 2.4G Wireless Receiver", "SINO WEALTH Gaming KB "]

    #Some mfs decided to add a trailing space at that name to troll me.

    # Find all devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # Print info on all devices (need to run as root):
    for device in devices:
        print(f"{device.path}\t{device.name}\t{device.phys}")
    internal_path = find_internal(devices, laptop_keyboard_name)
    if (internal_path == ""):
        print("Interal keyboard not found. Please adjust the laptop_keyboard_name variable in the script file.")
        exit(0)

    while 1:
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        external_path = find_external(devices, external_keyboard_names)
        print(external_path)
        if (external_path == ""):
            time.sleep(2)
        else:
            get_info(internal_path)

            # keygenerator = getKey()

            # tpad = evdev.InputDevice('/dev/input/event11')
            keybd = evdev.InputDevice(internal_path)

            # disable device
            keybd.grab()
            print("Grabbing keyboard!")

            # Print every key pressed, hang-loop:
            for event in keybd.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    print(evdev.categorize(event))

                    # ESC on the now dead keyboard kills the script and returns control
                    if evdev.categorize(event).keycode == "KEY_ESC":
                        break

            print("Ungrabbing keyboard!")
            keybd.ungrab()
