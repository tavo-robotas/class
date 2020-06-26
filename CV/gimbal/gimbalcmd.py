# Simple Gimbal Command Control
# By: Brandon
# v1.0 Date:07/19/2018

# To add commands simply type the HEX found at http://www.olliw.eu/storm32bgc-wiki/Serial_Communication.
# Example would look like 'HEX value here'+ crc or 'HEX value here' + data + crc.
# Follow the format in the command list.

# Library Initialization
import sys
import os
import struct
import time
import imutils
import serial
import binascii
import cv2 as cv
import math
import numpy as np
import pdb
from functools import reduce


from serial import SerialException

'''
WIP to do list
*Set COM outside script, easy  
*combine axis conversion functions into 1, QOL 
*Reduce global variable stuff, QOL
'''

######################Global variable declaration(User Specific)#######################
baud = 115200  # Having the wrong value here will cause serial communication issues.
com = 'COM5'  # Change this value to your COM port
crc = '3334'  # Non-mavlink CRC dummy value. Should not need to change!
sleeptime = [None, 0]  # In seconds. [Movement CMD delay, Non-movement CMD delay]

#   Pitch     Roll      Yaw
# [Min, Max, Min, Max, Min, Max]
axislimit = [None] * 6
axisloc = [47, 48, 54, 55, 61, 62]
safelimit = [-15, 15, -25, 25, -100, 100]

#     Pitch         Roll          Yaw
# [speed, accel, speed, accel, speed, accel]
speedparam = [None] * 6
speedloc = [49, 50, 56, 57, 63, 64]
safespeed = [60, 60, 60, 60, 100, 60]

dofinterval = [None] * 6
sleepmultiplier = [None] * 6
zeropoint = [None] * 3
axispos = [0] * 3

# Global array lists
paramlist = (axislimit, speedparam)
paramloc = (axisloc, speedloc)
safemodelist = (safelimit, safespeed)

# Global Flags
sleep = [False]
#######################################################################################
v_source = 1
capture = cv.VideoCapture(v_source)
# capture.set(3, 1280)
# capture.set(4, 720)
#
# h = capture.get(3)
# w = capture.get(4)

markers = []
alpha = 0.4
h_theta = 2.443  # rad
v_theta = 61.57


px_s = 0.006
py_s = 0.006
focal = 2.14
center = (0, 0)
point = (0, 0)

sensor_W = 4.22
sensor_H = 2.38
fx = 325.08
fy = 325.43

x_error_size = -0.005
y_error_size = 0.005

x_angle_storage = [0]
y_angle_storage = [0]

delay = int(1)
previous = int(0)

def f2b(fn):
    return struct.pack("f",fn)

def crc_accumulate(b, crcTmp):
    tmp = 0
    tmp = ( b ^ ( crcTmp & 0xff ) ) & 0xff
    tmp = ( tmp ^ ( tmp <<4 ) ) & 0xff
    crcTmp = ( (crcTmp >>8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4) ) & 0xffff
    return crcTmp


def get_crc(bstr):
    crcTmp = 0xffff
    for b in bstr :
        crcTmp = crc_accumulate(b,crcTmp)
    #return crcTmp
    #return struct.pack('>I', 0xffff & crcTmp)[:2]
    return struct.pack('I', 0xffff & crcTmp)[:2]

# def call(e):
#     pass
#
#
# cv.namedWindow('sense', cv.WINDOW_AUTOSIZE)
# cv.createTrackbar('LH', 'sense', 0, 255, call)
# cv.createTrackbar('LS', 'sense', 0, 255, call)
# cv.createTrackbar('LV', 'sense', 0, 255, call)
# cv.createTrackbar('UH', 'sense', 255, 255, call)
# cv.createTrackbar('US', 'sense', 255, 255, call)
# cv.createTrackbar('UV', 'sense', 255, 255, call)
#


# with np.load(os.getcwd() + '/data.npz') as file:
#     _, mtx, dist, r_m, t_m = [file[i] for i in ('ret', 'mtx', 'dist', 'rotation', 'translation')]
#     print(f"Intrinsic matrix:{mtx}")
#     print(f"distortion coeff:{dist}")
#
# def undistort(img, mtx, dist, w, h):
#     h, w = img.shape[:2]
#     nmtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
#     mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, nmtx, (w, h), 5)
#     dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
#
#     # crop the image
#     x, y, w, h = roi
#     #dst = dst[y:y + h, x:x + w]
#     return dst


#######################################################################################
def set_angle_storage(x, y):
    x_angle_storage.append(x)
    y_angle_storage.append(y)
    print(f'incoming x value is {x}')
    x_max = x_angle_storage[-2]+x_angle_storage[-1]
    y_max = y_angle_storage[-2]+y_angle_storage[-1]
    x_angle_storage[-1] = x_max
    y_angle_storage[-1] = y_max
    # max_find = lambda a,b: a+b
    # x_max = reduce(max_find,x_angle_storage)
    # y_max = reduce(max_find,y_angle_storage)

    print(f'from storage x -1 value is {x_angle_storage[-1]}')
    print(f'from storage x -2 value is {x_angle_storage[-2]}')
    print(f'from storage x max value is {x_max}')
    return x_max, y_max

# def get_angle_storage(angle):
#     if angle == 'x':
#         return x_angle_storage
#     if angle == 'y':
#         return x_angle_storage

def mark_event(ev, x, y, flags, param):
    if ev == cv.EVENT_LBUTTONDOWN:
        point = x, y
        markers.append((x, y))
        #cv.arrowedLine(frame, center, point, (255, 255, 255), 2)
        #cv.circle(frame, point, 10, (255, 0, 0), -1)

        cv.imshow('testas', uframe)

        target = distance((x_mid, y_mid), markers[-1])
        angles = get_angle(target)
        x, y = angles
        #print(f'x angle: {x}, y angle: {y}')
        xp, yp = set_angle_storage(x, y)

        print(f'storage x : {xp}')
        print(f'storage y : {yp}')

        setpitchrollyaw(yp, 0, -xp)
        # setpitch(angles[1] * -1)

def mark(coordinates, middle):
    (x, y) = coordinates
    (x_mid, y_mid) = middle
    markers.append((x, y))

    target = distance((x_mid, y_mid), markers[-1])
    angles = get_angle(target)
    x, y = angles
    xp, yp = set_angle_storage(x, y)

    print(f'storage x : {xp}')
    print(f'storage y : {yp}')

    setpitchrollyaw(yp, 0, -xp)


def distance(points, mark):
    x_c, y_c   = points
    x_im, y_im = mark

    print(f"x_mark: {x_im}, y_mark: {y_im}")
    # pdb.set_trace()
    # (200 - 320)* 0.0075
    x = (x_im - x_c)* px_s
    y = (y_im - y_c)* py_s
    # pdb.set_trace()h

    print(f"calculated x distance: {x}, y distance: {y}")

    return x, y
    #return tuple((a - b) for a, b in zip(points, mark))


def get_angle(coordinates):
    # returns radians
    x, y = coordinates
    theta_x = x/focal
    theta_y = y/focal

    # theta_x = x*(px_s/focal)
    # theta_y = y*(px_s/focal)
    # atan_x = math.atan(theta_x)
    # atan_y = math.atan(theta_y)
    #x_angle = math.degrees(atan_x)
    #y_angle = math.degrees(atan_y)

    #x_error = math.degrees(math.tan(x_error_size/focal))
    #y_error = math.degrees(math.tan(y_error_size/focal))

    x_angle = math.degrees(math.tan(theta_x))
    y_angle = math.degrees(math.tan(theta_y))

    print(f"calculated angles x: {x_angle}, y: {y_angle}")
    return x_angle, y_angle

    # x_error = math.degrees(math.atan(((2 * x) * math.tan(h_theta)) / frame.shape[1]))
    # y_error = math.degrees(math.atan(((2 * y) * math.tan(v_theta)) / frame.shape[0]))

    # return x_error, y_error


# Initializes Serial
def serialinit():
    global ser
    try:
        ser = (serial.Serial(
            port=com,
            baudrate=baud,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1.0,  # IMPORTANT, can be lower or higher
            inter_byte_timeout=0.1))
    except SerialException:
        sys.exit('Serial port unavailable, script cancelled!')
    ser.close()
    return (ser)


######################################################
##################COMMAND LIST BELOW##################
######################################################
def getversionstr():
    cmd = bytes.fromhex('FA0002' + crc)
    cmdexecute(cmd, sleep)


def getparameter(number):
    hexnum = dectohex(number)
    cmd = bytes.fromhex('FA0203' + hexnum + crc)
    response = cmdexecute(cmd, sleep)
    return (response)


def homeall():
    x_angle_storage[:] = [0]
    y_angle_storage[:] = [0]
    setpitchrollyaw(0, 0, 0)


def homepitch():
    setpitch(0)


def homeroll():
    setpitch(0)


def homeyaw():
    setyaw(0)


def setpitch(pitchin):
    pitch = pitchconvert(pitchin)
    cmd = bytes.fromhex('FA020A' + pitch + crc)
    cmdexecute(cmd, sleep)


def setroll(rollin):
    roll = rollconvert(rollin)
    cmd = bytes.fromhex('FA020B' + roll + crc)
    cmdexecute(cmd, sleep)


def setyaw(yawin):
    yaw = yawconvert(yawin)
    cmd = bytes.fromhex('FA020C' + yaw + crc)
    cmdexecute(cmd, sleep)


def setpitchrollyaw(pitchin, rollin, yawin):
    pitch = pitchconvert(pitchin)
    roll = rollconvert(rollin)
    yaw = yawconvert(yawin)
    # 0xFA 0x06 0x12
    cmd = bytes.fromhex('FA0612' + pitch + roll + yaw + crc)
    cmdexecute(cmd, sleep)


def setangle(pitch, roll, yaw):
    # 0xFA 0x0E 0x11
    # float1 float2 float3 flags-byte type-byte crc-low-byte crc-high-byte
    out = b'\x0e\x11' + f2b(pitch) + f2b(roll) + f2b(yaw) + b'\x00\x00'
    out = b'\xfa' + out + bytes.fromhex(crc)
    cmdexecute(out, sleep)


######################################################
######################################################

# Checks serial response
def responsetest(ser):
    ser.open()
    ser.write(b't')
    response = ser.readline()
    # print(response)
    if response == b'o':
        # print("Test response good!")
        safemode = False
    else:
        print("""
RESPONSE ERROR: Gimbal response INOP/bad, aspects of the script will 
be put into safe mode.  This will cause overall control inaccuracies. 
 Fixes: 
   1.) Restart Gimbal.
   2.) Disconnect any extra/unnecessary serial connections.
   3.) Re-connect and check gimbal Serial/COM connections.""")

        userstop = input("Would you like to continue anyways [Y/N]? ")
        if (userstop != 'y') and (userstop != 'Y'):
            sys.exit("Script cancelled.")
        else:
            safemode = True
    ser.close()
    return (safemode)


# Stores parameter data in pairs of two (ex:(min, max))
def paramstore(flag):
    param = [None] * 2
    for i in range(2):
        index = 0
        if flag == False:
            for j in range(0, 5, 2):
                param[0] = getparameter(paramloc[i][j])
                param[1] = getparameter(paramloc[i][j + 1])
                for k in param:
                    paramsnip = sniphex(k, 10, 14)  # Snips out the param value
                    paramflip = fliphex(paramsnip)  # Flips hex to High-Low
                    signeddec = int(paramflip, 16)  # Converts to decimal
                    paramlist[i][index] = (-(signeddec & 0x8000) | (
                                signeddec & 0x7fff)) / 10  # Converts signed decimal to negatives and shifts decimal point
                    index += 1
        else:
            for k in range(6):
                paramlist[i][k] = safemodelist[i][k]
    return (None)


# Calculates the deg -> decimal interval for each axis
def intervalcalc():
    index = 0
    # wiki link: http://www.olliw.eu/storm32bgc-wiki/Inputs_and_Functions#Rc_Input_Processing
    bound = 400  # Wiki states it should be +/-500, but 400 seems to work better (in my case)
    for i in range(0, 5, 2):
        if axislimit[i] > 0:
            zeropoint[index] = axislimit[i]
        else:
            zeropoint[index] = 0
        dofinterval[i] = bound / abs(axislimit[i])  # Min: interval amt to move 1 degree
        boundadjust = bound - ((bound / abs(axislimit[i + 1])) * zeropoint[index])  # Accounts for zeropoint change.
        dofinterval[i + 1] = boundadjust / abs(axislimit[i + 1])  # Max: interval amt to move 1 degree
        index += 1
    return (zeropoint)


# Calculates sleeptime multiplier depending on speed parameters for all axises
'''Note to self: Split speed and accel interval into separate arrays'''


def sleepmultipliercalc():
    for i in range(0, 6, 2):
        sleepmultiplier[i] = ((.05) / (speedparam[i] / (50)))
        sleepmultiplier[i + 1] = (.05 * speedparam[i + 1])


# Data display for important info
def datalog(safemode):
    print('''\
*******************************
   Storm32 GIMBAL CONTROLLER
===============================	
        Min    Max              
Pitch:[{pmin}, {pmax}]        
Roll :[{rmin}, {rmax}]        
Yaw  :[{ymin}, {ymax}]
*******************************
SafeMode Active: [{sm}]   
*******************************                               
Port: {port}  Baud: [{br}]           
*******************************
DataLog:\
'''.format(pmin=axislimit[0], pmax=axislimit[1], rmin=axislimit[2],
           rmax=axislimit[3], ymin=axislimit[4], ymax=axislimit[5],
           sm=safemode, port=com, br=baud))
    return (None)


###########################Frequently used equations/code##################################
# Decimal to 4byte HEX
def dectohex(value):
    hexnum = hex(value)[2:]
    length = (len(hexnum))
    while length <= 3:
        hexnum = '0' + hexnum
        length = (len(hexnum))
    hexflip = fliphex(hexnum)
    return (hexflip)


# Flips HEX bytes, 2 bytes at a time
def fliphex(bytes):
    formatbytes = "".join(reversed([bytes[i:i + 2] for i in range(0, len(bytes), 2)]))
    return (formatbytes)


# snips out param DATA bytes
def sniphex(snipbytes, start, stop):
    snipbytes = (binascii.b2a_hex(snipbytes).decode("utf-8"))[start:stop]
    return (snipbytes)


###########################################################################################
###########################################################################################

# Checks input to see if it's in-bounds
def pitchincheck(pitchin):
    if pitchin < axislimit[0]:
        pitchin = axislimit[0]
        print('Pitch exceeds min travel parameter! Input was adjusted to max travel distance.')
    elif pitchin > axislimit[1]:
        pitchin = axislimit[1]
        print('Pitch exceeds max travel parameter! Input was adjusted to max travel distance.')
    #pdb.set_trace()
    return (pitchin)


def rollincheck(rollin):
    if rollin < axislimit[2]:
        rollin = axislimit[2]
        print('Roll exceeds min travel parameter! Input was adjusted to max travel distance.')
    elif rollin > axislimit[3]:
        rollin = axislimit[3]
        print('Roll exceeds max travel parameter! Input was adjusted to max travel distance.')
    return (rollin)


def yawincheck(yawin):
    if yawin < axislimit[4]:
        yawin = axislimit[4]
        print('Yaw exceeds min travel parameter! Input was adjusted to max travel distance.')
    elif yawin > axislimit[5]:
        yawin = axislimit[5]
        print('Yaw exceeds max travel parameter! Input was adjusted to max travel distance.')
    return (yawin)


#######################################################################################################
#######################################################################################################

'''Combine into 1 function'''


# Converts input to useable HEX data for gimbal (Only for certain commands!)
def pitchconvert(pitchin):
    pitchin = pitchincheck(pitchin)
    sleepinput = abs(pitchin - axispos[0])
    if pitchin <= zeropoint[0]:
        pitchraw = int(1500 + (dofinterval[0] * pitchin))  # Converts user roll input to movement distance
    else:
        pitchraw = int(1500 + (dofinterval[1] * pitchin))
    pitch = dectohex(pitchraw)  # Re-orders bytes to Low-High in pairs of two
    # print(pitch)
    sleeptime[0] = ((sleepmultiplier[0] * sleepinput) + sleepmultiplier[1])
    axispos[0] = pitchin
    sleep[0] = True
    print('Pitch axis:', pitchin, end='°\n')
    return (pitch)


def rollconvert(rollin):
    rollin = rollincheck(rollin)
    sleepinput = abs(rollin - axispos[1])
    if rollin <= zeropoint[1]:
        rollraw = int(1500 + (dofinterval[2] * rollin))  # Converts user roll input to movement distance
    else:
        rollraw = int(1500 + (dofinterval[3] * rollin))
    roll = dectohex(rollraw)  # Re-orders bytes to Low-High in pairs of two
    # print(roll)
    sleeptime[0] = abs((sleepmultiplier[2] * sleepinput) + sleepmultiplier[3])
    axispos[1] = rollin
    sleep[0] = True
    print('Roll axis:', rollin, end='°\n')
    return (roll)


def yawconvert(yawin):
    yawin = yawincheck(yawin)
    sleepinput = abs(yawin - axispos[2])
    if yawin <= zeropoint[2]:
        yawraw = int(1500 + (dofinterval[4] * yawin))  # Converts user roll input to movement distance
    else:
        yawraw = int(1500 + (dofinterval[5] * yawin))
    yaw = dectohex(yawraw)  # Re-orders bytes to Low-High in pairs of two
    # print(yaw)
    sleeptime[0] = abs((sleepmultiplier[4] * sleepinput) + sleepmultiplier[5])
    axispos[2] = yawin
    sleep[0] = True
    print('Yaw axis:', yawin, end='°\n')
    return (yaw)


###########################################################################################################################
###########################################################################################################################

# Executes commands
def cmdexecute(cmd, sleep):
    ser.open()
    if sleep[0] == False:
        ser.write(cmd)
        response = (ser.readline())
        #time.sleep(sleeptime[1])
        # print(response)
    else:
        ser.write(cmd)
        response = (ser.readline())
        print('Gimbal moveing wait', end="...")
        sys.stdout.flush()
        #time.sleep(sleeptime[0])
        print('Done', end="\n==========================\n")
    sleep[0] = False
    ser.close()
    return (response)


# Intializes script
def main():
    print('Initializing...', end='')
    sys.stdout.flush()
    ser = serialinit()
    safemode = responsetest(ser)
    paramstore(safemode)
    sleepmultipliercalc()
    intervalcalc()
    print("Done")
    datalog(safemode)
    array = ['helloworld']


if __name__ == "__main__":
    main()
else:
    main()

# Test script here
setpitch(25)
# setroll(0)
# setyaw(0)
# homeall()

# while capture.isOpened():
#     retain, uframe = capture.read()
#     h, w = uframe.shape[:2]
#     #uframe = undistort(frame, mtx, dist, w, h)
#     # uframe = cv.transpose(uframe)
#     # uframe = cv.flip(uframe, flipCode=1)
#     #frame = cv.flip(frame, 0)
#
#     # uframe = uframe[0:, 0:880]
#     # memory leak ?
#     overlay = uframe.copy()
#
#     x_min = 0
#     x_max = int(uframe.shape[1])
#     x_mid = 325.71  # int(frame.shape[1] / 2)
#     y_min = 0
#     y_max = int(uframe.shape[0])
#     y_mid = 254.07  # int(frame.shape[0] / 2)
#     middle_point = x_mid, y_mid
#     cv.line(uframe, (x_min, int(y_mid)), (x_max, int(y_mid)), (0, 0, 255), 2)
#     cv.line(uframe, (int(x_mid), y_min), (int(x_mid), y_max), (0, 0, 255), 2)
#     cv.circle(uframe, (int(x_mid), int(y_mid)), 10, (0, 0, 255), 2)
#
#     if retain:
#
#         blurred = cv.GaussianBlur(overlay, (13, 13), 0)
#         hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
#
#         # l_h = cv.getTrackbarPos('LH', 'sense')
#         # l_s = cv.getTrackbarPos('LS', 'sense')
#         # l_v = cv.getTrackbarPos('LV', 'sense')
#         # u_h = cv.getTrackbarPos('UH', 'sense')
#         # u_s = cv.getTrackbarPos('US', 'sense')
#         # u_v = cv.getTrackbarPos('UV', 'sense')
#
#         l_h = 105
#         l_s = 110
#         l_v = 130
#         u_h = 255
#         u_s = 255
#         u_v = 255
#         lower_bound = np.array([l_h, l_s, l_v])
#         upper_bound = np.array([u_h, u_s, u_v])
#
#         mask = cv.inRange(hsv, lower_bound, upper_bound)
#         # cv erode documentation
#         mask = cv.erode(mask, None, iterations=4)
#         # cv dilate documentation
#         mask = cv.dilate(mask, None, iterations=4)
#         result = cv.bitwise_and(overlay, overlay, mask=mask)
#         outlines = cv.findContours(
#             mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#         contours = imutils.grab_contours(outlines)
#         if len(contours) > 0:
#             # print(contours)
#             c = max(contours, key=cv.contourArea)
#             ((x, y), radius) = cv.minEnclosingCircle(c)
#             M = cv.moments(c)
#             center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
#
#             if radius > 10:
#
#                 cv.circle(uframe, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#                 target = (int(x), int(y))
#                 #print(target)
#                 # holder.append(target)
#                 # if len(holder) > 20:
#                 #     for entry in holder:
#                 #         print(entry)
#                 if time.process_time() - previous > delay:
#                     mark(target, middle_point)
#                     #print(target)
#                     previous = time.process_time()
#
#
#
#
#         cv.setMouseCallback('testas', mark_event)
#         cv.imshow('overlay', mask)
#         cv.imshow('testas', uframe)
#
#         key = cv.waitKey(1)
#         if key == ord('h'):
#             homeall()
#         if key == 27:
#             break
#     else:
#         break
#
# capture.release()
# cv.destroyAllWindows()
