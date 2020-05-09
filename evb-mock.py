import serial
import tkinter
import sys
import time

KEY_DESCRIPTION = [
    "S1: FIREFOX     ",
    "S2: HOME DIR    ",
    "S3: PK.EDU.PL   ",
    "S4: THUNDERBIRD ",
    "S5: END THIS APP",
    "S6: SYSTEM SLEEP",
    "S7: SYS REBOOT  ",
    "S8: SYS SHUTDOWN"
] 

volume_changed = False
new_volume_level = 0

key_pressed = False
key_id = 0

key_description_index = 7

def button_callback(i):
    global key_pressed
    global key_id
    key_pressed = True
    key_id = i

def scale_callback(val):
    global volume_changed
    global new_volume_level
    volume_changed = True
    new_volume_level = int(val)

def rgb_to_hex(rgb):
    return '#' + '%02x%02x%02x' % rgb

window = tkinter.Tk()
window.title("EvB 5.1 v5 simulator")
window.resizable(False, False)

tkinter.Label(window, text="Shortcut buttons:").grid(row=0, column=0, columnspan=9)
for i in range(1, 9):
    tkinter.Button(window, text="S" + str(i), command=lambda i=i: button_callback(i)).grid(row=1, column=i)

tkinter.Label(window, text="HD44780:").grid(row=2, column=0, columnspan=9)
hd_row1 = tkinter.StringVar()
hd_row1.set("C:0   T:0  R:0  ")
tkinter.Label(window, textvariable=hd_row1, font="monospace 16", background="green").grid(row=3, column=0, columnspan=9)
hd_row2 = tkinter.StringVar()
hd_row2.set("S1: FIREFOX     ")
tkinter.Label(window, textvariable=hd_row2, font="monospace 16", background="green").grid(row=4, column=0, columnspan=9)

tkinter.Label(window, text="LED diodes:").grid(row=5, column=0, columnspan=9)
diodes = []
for i in range(1, 9):
    diodes.append(tkinter.Frame(window, width=20, height=20, background="red"))
    diodes[i - 1].grid(row=6, column=i)

tkinter.Label(window, text="RGB diode:").grid(row=7, column=0, columnspan=9)
rgb_diode = tkinter.Frame(window, width=30, height=30, background="red")
rgb_diode.grid(row=8, column=1, columnspan=9)

tkinter.Label(window, text="ADC potentiometer:").grid(row=9, column=0, columnspan=9)
tkinter.Scale(window, from_=0, to=100, tickinterval=20, length=250, orient=tkinter.HORIZONTAL, command=scale_callback).grid(row=10, column=0, columnspan=9)

def display_volume_level(volume_level):
    for i, val in enumerate(range(6, 100, 12)):
        if volume_level > val:
            diodes[i].config(background="#FF0000")
        else:
            diodes[i].config(background="#550000")

def key_description_loop():
    global key_description_index
    key_description_index = (key_description_index + 1) % 8
    hd_row2.set(KEY_DESCRIPTION[key_description_index])
    window.after(3000, key_description_loop)

def system_information_loop():
    with serial.Serial('/dev/pts/' + sys.argv[1], 115200) as ser:
        # GET AND DISPLAY SYSTEM USAGE
        ser.write("T".encode())
        cpu_usage       = ord(ser.read())
        cpu_temperature = ord(ser.read())
        ram_usage       = ord(ser.read())
        msg = "C:" + str(cpu_usage) + " " * (4 - len(str(cpu_usage))) +\
                "T:" + str(cpu_temperature) + " " * (3 - len(str(cpu_temperature))) +\
                "R:" + str(ram_usage) + " " * (3 - len(str(ram_usage)))
        hd_row1.set(msg)

        # GET AND DISPLAY VOLUME LEVEL
        ser.write("A".encode())
        current_volume_level = ord(ser.read())
        display_volume_level(current_volume_level)
    window.after(1000, system_information_loop)

def control_loop():
    with serial.Serial('/dev/pts/' + sys.argv[1], 115200) as ser:
        global volume_changed
        global new_volume_level

        global key_pressed
        global key_id
        
        # HANDLE BUTTONS
        if key_pressed:
            ser.write("K".encode())
            ser.write(bytes([key_id]))
            key_pressed = False
            if key_id == 5:
                window.destroy()

        # CHANGE VOLUME LEVEL
        if volume_changed:
            ser.write("S".encode())
            ser.write(bytes([new_volume_level]))
            current_volume_level = new_volume_level
            display_volume_level(current_volume_level)
            volume_changed = False
    window.after(100, control_loop)

def rgb_diode_loop():
    # DISPLAY RGB DIODE
    with serial.Serial('/dev/pts/' + sys.argv[1], 115200) as ser:
        ser.write("V".encode())
        red   = ord(ser.read())
        green = ord(ser.read())
        blue  = ord(ser.read())
        hex_color = rgb_to_hex((red, green, blue))
        rgb_diode.config(background=hex_color)
    window.after(20, rgb_diode_loop)

key_description_loop()
system_information_loop()
control_loop()
rgb_diode_loop()

window.mainloop()