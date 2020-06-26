# Test of MM control over BLE Nordic nRF5* UART
# with picam blob detection on gimbal
# when the gimbal reaches its angle limits it asks the MM to move.
# v2 attempts to split into independent threads for gimbal and MM
# Wes Freeman 2018. Uses:
# Adafruit library by Tony DiCola
# imutils by Adrian Rosebrock

import binascii
import time
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import numpy as np
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import serial
import crc16
from threading import Thread
from pick import pick  # for UART list

# serial to STorM32
ser = serial.Serial(
    port='/dev/ttyAMA0',  # or ttyS0
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


class globs():
    yawServo = 1500
    pitchServo = 1500
    blobRadius = 0.0


# intToHex func changes 8b signed integer into 8bit hex,
# strips off the "0x" part,
# and makes sure there's 2 digits; "0f" not "f"
# used by MM_motion for BLE command prep
def intToHex(num):
    # 2's complement signed version of hex:
    result = hex((num + (1 << 8)) % (1 << 8))
    # strips off the "0x" part:
    result = result[2:]
    # if just one char:
    if len(result) < 2:
        result = '0' + result  # add leading zero
    return result


# MM_motion produces byte strings for motion command
# from signed int inputs
def MM_motion(a, b, c):
    # (abc = strafe, fwd, turn)
    # implement channel rules
    prefix = 0  # prefix
    # look up table for active channels:
    # 8 states
    if (a == 0 and b == 0 and c == 0):  # 0: no movement
        prefix = '02'
        a = 1
        b = 1
        c = 1
    elif (a == 0 and b == 0 and c != 0):  # 1: turn only
        prefix = '02'
        a = 1
        b = 2
    elif (a == 0 and b != 0 and c == 0):  # 2: fwd only
        prefix = '02'
        a = 2
        c = 1
    elif (a == 0 and b != 0 and c != 0):  # 3: fwd + turn
        prefix = '02'
        a = 3
    elif (a != 0 and b == 0 and c == 0):  # 4: strafe only
        prefix = '03'
        b = 1
        c = 1
    elif (a != 0 and b == 0 and c != 0):  # 5: strafe + turn
        prefix = '03'
        b = 2
    elif (a != 0 and b != 0 and c == 0):  # 6: strafe + fwd
        prefix = '04'
        c = 1
    elif (a != 0 and b != 0 and c != 0):  # 7: all 3
        prefix = '05'
    else:
        print
    'LUT error\r'

    # convert vars to hex byte format:
    strafe = intToHex(a)
    fwd = intToHex(b)
    turn = intToHex(c)

    # start building command string:
    cmd = prefix
    # append the command:
    cmd += '06'
    # append vars
    cmd += strafe
    cmd += fwd
    cmd += turn

    checksum = 6  # starting value from command '06'
    # add prefix to checksum
    checksum += int(prefix, 16)

    # get checksum of control string
    checksum += int(strafe, 16)
    checksum += int(fwd, 16)
    checksum += int(turn, 16)

    # add 1 because MM expects it for unknown reason:
    checksum += 1
    # another fiddle factor for MM odd behaviour with >1 -ve value:
    if (a < 0 and b < 0): checksum += 1

    checksum %= 256  # roll over if bigger than 8b
    # print ('checksum total:', checksum)

    cmd += intToHex(checksum)
    cmd += intToHex(0)
    # print('cmd string:', cmd)
    return cmd


# intToBytes func splits a 16b integer into 2 8bit hex,
# strips off the "0x" part,
# and makes sure there's 2 digits; "0f" not "f"
# used to help construct serial commands for gimbal controller
def intToBytes(num):
    high = hex(num >> 8)
    high = high[2:]  # trim off 0x
    if len(high) < 2:  # if just one char
        high = '0' + high  # add leading zero
    low = hex(num & 0xFF)
    low = low[2:]
    if len(low) < 2:  # if just one char
        low = '0' + low  # add leading zero
    return high, low


# YawPitch func sends Yaw or Pitch (or roll) command to gimbal controller
# 'angle' is like a servo not degrees:
# values from 700 to 2300, range 1600, centre 700+800 = 1500
def YawPitch(command, angle):
    cmdStart = 'FA'  # standard startsign, not included in CRC!

    cmd = command  # copy it so we can modify the copy

    # convert to hex bytes format:
    angleHigh, angleLow = intToBytes(angle)

    # add angle bytes to control hex string
    cmd += angleLow
    cmd += angleHigh

    # get CRC of control string
    cmd = str.encode(cmd)  # to bytes format
    crc = crc16.crc16xmodem(cmd)  # CRC-CCITT (XModem) format
    crcHigh, crcLow = intToBytes(crc)

    # build complete control string:
    serialOut = cmdStart + cmd + crcLow + crcHigh
    serialOut = serialOut.upper()  # uppercase
    serialOut = str.encode(serialOut)  # convert to bytes
    # print 'to gimbal:', serialOut, '\r'

    # reformat from "0f" to "\x0f" and send
    ser.write(binascii.unhexlify(serialOut))


# run once: -----------------------------------------------------------
# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def ble_MM():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART devices...')
    adapter.start_scan()

    known_uarts = set()

    time_end = time.time() + 10  # search for x secs
    while time.time() < time_end:
        # Call UART.find_devices to get a list of any UART devices that
        # have been found.  This call will quickly return results and does
        # not wait for devices to appear.
        found = set(UART.find_devices())
        # Check for new devices that haven't been seen yet and print out
        # their name and ID (MAC address on Linux, GUID on OSX).
        new = found - known_uarts
        for device in new:
            print('Found UART: {0} [{1}]'.format(device.name, device.id))
        known_uarts.update(new)
        # Sleep for a second and see if new devices have appeared.
        time.sleep(1.0)

    # Make sure scanning is stopped before exiting.
    adapter.stop_scan()
    devNames = []
    UARTlist = []
    for device in known_uarts:
        devNames.append(device.name)
        UARTlist.append(device)  # copy set to list to make it inexable

    title = 'Please choose Mekamon to control: '
    option, index = pick(devNames, title)
    print
    option
    print
    index

    device = UARTlist[index]

    print('Connecting to device...')
    device.connect(timeout_sec=10)

    print('Discovering services...')
    UART.discover(device)

    # Once service discovery is complete create an instance of the service
    # and start interacting with it.
    uart = UART(device)

    # ------------- BT init done ---------------------------------------

    # list of initial MM messages.
    msgList = ('02101300',  # init1
               '0307010c00',  # init2
               '02060101010c00',  # motion neutral
               )

    for msg in msgList:
        message = str.encode(msg)  # convert to bytes
        print
        'to MM: ', message, '\r'
        message = binascii.unhexlify(message)
        uart.write(message)

    limit = 80  # MM motion magnitude, max range -127 .. 127? 8b signed
    strafe = 0  # no walking yet
    # now repeatedly send movement commands based on what camera and gimbal are doing:
    while 1:
        # blob too far = walk toward, blob too close = walk backward:
        if (globs.blobRadius > 10 and globs.blobRadius < 20):
            fwd = 20
        elif (globs.blobRadius > 50):
            fwd = -20
        else:
            fwd = 0

        # turn if gimbal near its yaw limit, to try and bring blob back in view
        if (globs.yawServo > 1650):
            print
            'turning right \r'
            turn = -20  # arbitrarily chosen low value; yaw isn't very controllable on MM
        elif (globs.yawServo < 1350):
            print
            'turning left \r'
            turn = 20
        else:
            turn = 0

        # print  'strafe: %d fwd: %d turn: %d' % (strafe, fwd, turn), '\r'

        message = MM_motion(strafe, fwd, turn)

        print
        'to MM: ', message, '\r'
        message = str.encode(message)  # convert to bytes
        message = binascii.unhexlify(message)
        uart.write(message)


def cameraGimbal():
    #  camera setup  ---------------------------------------------------
    camera = PiCamera()
    resX = 320
    resY = 240
    camera.resolution = (resX, resY)
    camera.framerate = 5  # <<<<<< TIMING
    camera.hflip = False  # cam mounted upside-down?
    camera.vflip = False
    rawCapture = PiRGBArray(camera, size=(resX, resY))

    frameCount = 0

    # blob definition  ---------------------------------------------------
    # define the lower and upper boundaries of the object colour in HSV
    # use www.colorizer.org or similar to find suitable values
    # colorizer uses 0-360 for H, 0-100 for S & V
    # OpenCV uses  H: 0 - 180, S: 0 - 255, V: 0 - 255.
    # convert H: * 180/360
    # convert S & V: * 255/100
    colourLower = (95, 79, 23)  # using gpick on Ubuntu on camera feed
    colourUpper = (105, 255, 189)

    # gimbal setup   ---------------------------------------------------
    # default servo vals in globs class

    # max angle in degrees
    # ideally this should correspond to camera FOV
    maxYawDegrees = 32
    maxPitchDegrees = 20
    # servo range out of 1600 depends on mapping in controller
    # currently yaw is -45 to +45
    # pitch is -45 to +45
    # maxYaw= maxYawDegrees/90 TODO
    maxYawServo = 400
    maxPitchServo = 400

    # Storm commands:

    # CMD_GETVERSION (#1) format:
    # 0xFA 0x00 0x01 crc-low-byte crc-high-byte
    CMD_GETVERSION = '0001'  # 16b command without CRC part

    # CMD_SETYAW (#12)
    # 0xFA 0x02 0x0C data-low-byte data-high-byte crc-low-byte crc-high-byte
    CMD_SETYAW = '020C'  # 16b command without CRC part

    # CMD_SETPITCH (#10)
    # 0xFA 0x02 0x0A data-low-byte data-high-byte crc-low-byte crc-high-byte
    CMD_SETPITCH = '020A'  # 16b command without CRC part

    # CMD_SETANGLE (#17)
    # 0xFA 0x0E 0x11 float1 float2 float3 flags-byte type-byte crc-low-byte crc-high-byte

    time.sleep(20)  # allow time for BLE menu

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array
        # print 'frame', frameCount, '\r'
        # stdscr.addstr("frame", frameCount)
        frameCount += 1

        # OPENCV stuff:
        # convert frame to HSV colour
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # mask the colour, then dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, colourLower, colourUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), globs.blobRadius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the blobRadius meets a minimum size
            if globs.blobRadius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)), int(globs.blobRadius),
                           (0, 255, 255), 2)
                cv2.circle(image, center, 5, (0, 0, 255), -1)

                # split location of object:
                objX, objY = center

                # convert to angle
                # x is 0-320 px
                # angle is -32 - +32
                # offset so centre is 0,0:
                # runs from -160 to +160 instead of 0-320
                objX = int(objX - (resX / 2))
                objY = int(objY - (resY / 2))
                print
                'centre: ', objX, objY, 'blobRadius: ', globs.blobRadius, '\r'
                # if the position is off-centre by significant amount:
                if abs(objX) > resX * 0.05:
                    # convert position to degrees
                    yawDegrees = float(objX * maxYawDegrees / resX)
                    # convert to servo vals:
                    # from 700 to 2300, range 1600,
                    # centre 700+800 = 1500
                    yawDegrees *= -1  # reverse
                    globs.yawServo = yawDegrees * (maxYawServo / maxYawDegrees)
                    globs.yawServo = int(globs.yawServo + 1500)

                if abs(objY) > resY * 0.05:
                    # convert position to degrees
                    pitchDegrees = float(objY * maxPitchDegrees / resY)
                    # convert to servo vals:
                    globs.pitchServo = pitchDegrees * (maxPitchServo / maxPitchDegrees)
                    globs.pitchServo = int(globs.pitchServo + 1500)

            else:
                print
                'cam: blob too small \r'
                # (leave gimbal where it is)
        else:
            print
            'cam: no blob found \r'
            # reset gimbal to centre if no object:
            globs.pitchServo = 1500
            globs.yawServo = 1500

        # print 'gimbal yawServo:', globs.yawServo, '\r'
        # print 'gimbal pitchServo:', globs.pitchServo, '\r'

        # Gimbal control
        YawPitch(CMD_SETPITCH, globs.pitchServo)
        YawPitch(CMD_SETYAW, globs.yawServo)

        # DISPLAY TO WINDOW if headed
        # cv2.imshow("camera", image)
        kbd = cv2.waitKey(1)  # this is actually necessary!

        rawCapture.seek(0)  #
        rawCapture.truncate(0)  # clear the stream in preparation for the next frame

        if (kbd == 27):  # escape key
            print
            'cameraGimbal exiting \r'
            camera.close()
            cv2.destroyAllWindows()
            # Gimbal reset
            globs.pitchServo = 1500
            globs.yawServo = 1500
            YawPitch(CMD_SETPITCH, globs.pitchServo)
            YawPitch(CMD_SETYAW, globs.yawServo)
            break  # out of frame loop and function


# MAIN: ----------------------------------------


# start the camera + openCV + gimbal loop in it's own thread:
t1 = Thread(target=cameraGimbal, args=())
t1.start()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
# -
# This thread connects to BLE then loops sending MM commands,
# based on global vars from gimbal
ble.run_mainloop_with(ble_MM)





