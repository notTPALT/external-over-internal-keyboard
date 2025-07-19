Forked from [impaktor/disable-keyboard](https://github.com/impaktor/disable-keyboard)

# external-over-internal-keyboard

## Description

Disable laptop keyboard automatically whenever an external one is connected.

To re-enable the laptop keyboard, either:
- Cancel the script.
- Disconnect all external keyboards whose names added into the script and then press ESC (configurable).

## Installation

Depends on python and python-evdev package ([docs](https://python-evdev.readthedocs.io/en/latest/tutorial.html)) in Arch Linux.


## Usage
The command: `python external-over-internal-keyboard.py`

- Run the command once (with root privilege), it will print all devices connected to/on your laptop.
- Copy-paste the name of your internal keyboard to variable `internal_keyboard_name` in the script.
- Connect your external keyboard(s), get their names by running the script again, and paste those into the `external_keyboard_names` array.
- Now the script should be functionable from now on.


## License
Released under my basement.
