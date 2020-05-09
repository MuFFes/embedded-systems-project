import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
import serial
import subprocess
import sched
import time
import sys
import os


with serial.Serial('/dev/pts/' + sys.argv[1], 115200) as ser:
    red   = 0
    green = 0
    blue  = 0
    cpu_usage       = 0
    cpu_temperature = 0
    mem_usage       = 0
    volume_level    = 0

    # Variables needed for color calculation:
    window = Gdk.get_default_root_window()
    
    display = Gdk.Display.get_default()
    monitor = display.get_primary_monitor()
    geometry = monitor.get_geometry()
    scale_factor = monitor.get_scale_factor()
    screen_width = scale_factor * geometry.width
    screen_height = scale_factor * geometry.height

    offset = 50
    border = 50
    area_width  = screen_width  - border * 2
    area_height = screen_height - border * 2
    amount_of_pixels = (area_width // offset + 1) * (area_height // offset + 1)

    # Main loop:
    while (True):
        header = ser.read().decode()
        # ZAD 1:
        if header == 'S':
            new_volume = ord(ser.read())
            os.popen("pulsemixer --set-volume " + str(new_volume))

        # ZAD 2:
        elif header == 'A':
            volume_level = int(os.popen("pulsemixer --get-volume").read().split()[0])
            ser.write(bytes([volume_level]))

        # ZAD 3:
        elif header == 'T':
            ser.write(bytes([cpu_usage]))
            ser.write(bytes([cpu_temperature]))
            ser.write(bytes([mem_usage]))

            cpu_usage = int(float(os.popen("top -bn 2 -d 0.001 | grep 'Cpu(s)' | tail -n 1 | awk '{print $2+$4}'").read()))
            cpu_temperature = int(float(os.popen("cat /sys/class/thermal/thermal_zone0/temp | awk '{print $0/1000}'").read()))
            mem_usage = int(float(os.popen("free | grep Mem | awk '{print $3/$2*100}'").read()))

        # ZAD 4:
        elif header == 'K':
            key_id = ord(ser.read())
            if key_id == 1:
                os.system("firefox")
            elif key_id == 2:
                os.system("xdg-open ~")
            elif key_id == 3:
                os.system("xdg-open https://pk.edu.pl")
            elif key_id == 4:
                os.system("thunderbird")
            elif key_id == 5:
                os.system("killall socat")
            elif key_id == 6:
                os.system("reboot")
            elif key_id == 7:
                os.system("systemctl suspend")
            elif key_id == 8:
                os.system("shutdown -P now")

        # ZAD 6:
        elif header == 'V':
            ser.write(bytes([int(red)]))
            ser.write(bytes([int(green)]))
            ser.write(bytes([int(blue)]))

            pixbuf = Gdk.pixbuf_get_from_window(window, border, border, screen_width - border * 2, screen_height - border * 2)
            pixels = pixbuf.get_pixels()
            rowstride = pixbuf.get_rowstride()

            red = 0
            green = 0
            blue = 0

            for x in range(0, area_width, offset):
                for y in range(0, area_height, offset): 
                    p = x * 3 + y * rowstride
                    red += pixels[p]
                    green += pixels[p + 1]
                    blue += pixels[p + 2]

            red //= amount_of_pixels
            green //= amount_of_pixels
            blue //= amount_of_pixels

