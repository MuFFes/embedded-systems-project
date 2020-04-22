import serial

with serial.Serial('/dev/ttyUSB0', 9600) as ser:
    while (header = ser.read()):
        # ZAD 1:
        if header == 'S':
            new_volume = ser.read()
            ## TODO: set system volume level to received value
        # ZAD 2:
        elif header == 'A':
            ## TODO: get system volume level and send - ser.write()

        # ZAD 3:
        elif header == 'T':
            ## TODO: get system cpu usage, cpu temperature and ram usage and send - ser.write()

        # ZAD 4:
        elif header == 'K':
            key_id = ser.read()
            if key_id == 1:
            elif key_id == 2:
            elif key_id == 3:
            elif key_id == 4:
            elif key_id == 5:
            elif key_id == 6:
            elif key_id == 7:
            elif key_id == 8:
            ## TODO: Add key actions

        # ZAD 6:
        elif header == 'V':
            ## TODO: Get average screen color and send - ser.write()

