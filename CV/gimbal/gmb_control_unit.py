from config_manager import load_use_case_config
from dataclasses import dataclass, field

import serial as spi
import numpy as np
import cv2 as cv
import binascii
import imutils
import struct
import time
import math
import sys
import os
import pdb

from byte2Hex import *


def get_default_values(e):
    print(e)


settings = {
    'bound': 115200,
    'com': 'COM5',
    'crc': '3334',
    'sleep': [False],
    'sleep_time': [None, 0],
    'axis_limit': [None] * 6,
    'axis_lock': [47, 48, 54, 55, 61, 62],
    'safe_limit': [-15, 15, -25, 25, -100, 100],
    'speed_params': [None] * 6,
    'speed_lock': [49, 50, 56, 57, 63, 64],
    'safe_speed': [60, 60, 60, 60, 100, 60],
    'dof_interval': [None] * 6,
    'sleep_multiplier': [None] * 6,
    'zero_point': [None] * 3,
    'axis_pos': [0] * 3
}

settings['param_list'] = (settings['axis_limit'], settings['speed_params'])
settings['param_lock'] = (settings['axis_lock'], settings['speed_lock'])
settings['safe_mode_list'] = (settings['safe_limit'], settings['safe_speed'])

@dataclass(frozen=False)
class ControlUnit:
    bound: int = None
    com: str = None
    # Non - mav link CRC dummy value. Should not need to change!
    crc: str = None
    # In seconds. [Movement CMD delay, Non-movement CMD delay]
    sleep_time: list = None
    axis_lock: list = None
    sleep: bool = None
    axis_limit: list = None
    axis_pos: list = None
    safe_limit: list = None
    speed_params: list = None
    speed_lock: list = None
    safe_speed: list = None
    dof_interval: list = None
    sleep_multiplier: list = None
    zero_point: list = None
    param_list: tuple = None
    param_lock: tuple = None
    safe_mode_list: tuple = None
    ser: object = None

    def __post_init__(self):
        self.serial_init()

    def get_parameter(self, number):
        hex_num = decto(number)
        cmd = bytes.fromhex('FA0203' + hex_num + self.crc)
        response = self.cmd_execute(cmd)
        return response

    def serial_init(self):
        print(self.bound)
        try:
            self.ser = (spi.Serial(
                port=self.com,
                baudrate=self.bound,
                parity=spi.PARITY_NONE,
                stopbits=spi.STOPBITS_ONE,
                bytesize=spi.EIGHTBITS,
                timeout=1.0,
                inter_byte_timeout=0.1
            ))
        except spi.SerialException:
            sys.exit('serial port is unavailable and script is cancelled')
        self.ser.close()

    # Checks serial response
    @staticmethod
    def response_test(ser):
        ser.open()
        ser.write(b't')
        response = ser.readline()
        # print(response)
        if response == b'o':
            # print("Test response good!")
            safe_mode = False
        else:
            print("""
                RESPONSE ERROR: gimbal response INOP/bad, aspects of the script will 
                be put into safe mode.  This will cause overall control inaccuracies. 
                Fixes: 
                    1.) Restart gimbal.
                    2.) Disconnect any extra/unnecessary serial connections.
                    3.) Re-connect and check gimbal Serial/COM connections.
                    """)

            user_stop = input("Would you like to continue anyways [Y/N]? ")
            if (user_stop != 'y') and (user_stop != 'Y'):
                sys.exit("Script cancelled.")
            else:
                safe_mode = True
        ser.close()
        return safe_mode

    # Stores parameter data in pairs of two (ex:(min, max))
    def param_store(self, flag):
        param = [None] * 2
        for i in range(2):
            index = 0
            if flag == False:
                for j in range(0, 5, 2):
                    param[0] = self.get_parameter(self.param_lock[i][j])
                    param[1] = self.get_parameter(self.param_lock[i][j + 1])
                    for k in param:
                        param_snip = snip(k, 10, 14)  # Snips out the param value
                        param_flip = flip(param_snip)  # Flips hex to High-Low
                        signed_dec = int(param_flip, 16)  # Converts to decimal
                        # Converts signed decimal to negatives and shifts decimal point
                        self.param_list[i][index] = (-(signed_dec & 0x8000) | (signed_dec & 0x7fff)) / 10
                        index += 1
            else:
                for k in range(6):
                    self.param_list[i][k] = self.safe_mode_list[i][k]
        return None

    def interval_calc(self):
        index = 0
        # wiki link: http://www.olliw.eu/storm32bgc-wiki/Inputs_and_Functions#Rc_Input_Processing
        bound = 400  # Wiki states it should be +/-500, but 400 seems to work better (in my case)
        for i in range(0, 5, 2):
            if self.axis_limit[i] > 0:
                self.zero_point[index] = self.axis_limit[i]
            else:
                self.zero_point[index] = 0
            self.dof_interval[i] = bound / abs(self.axis_limit[i])  # Min: interval amt to move 1 degree
            adjust = bound - (
                        (bound / abs(self.axis_limit[i + 1])) * self.zero_point[index])  # Accounts for zeropoint change.
            self.dof_interval[i + 1] = adjust / abs(self.axis_limit[i + 1])  # Max: interval amt to move 1 degree
            index += 1

    # Calculates sleeptime multiplier depending on speed parameters for all axises
    '''Note to self: Split speed and accel interval into separate arrays'''

    def sleep_multiplier_calc(self):
        for i in range(0, 6, 2):
            self.sleep_multiplier[i] = (.05 / (self.speed_params[i] / 50))
            self.sleep_multiplier[i + 1] = (.05 * self.speed_params[i + 1])

    def data_log(self, safe_mode):
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
    '''.format(pmin=self.axis_limit[0], pmax=self.axis_limit[1], rmin=self.axis_limit[2],
               rmax=self.axis_limit[3], ymin=self.axis_limit[4], ymax=self.axis_limit[5],
               sm=safe_mode, port=self.com, br=self.bound))
        return None

    def cmd_execute(self, cmd):
        self.ser.open()
        if not self.sleep[0]:
            self.ser.write(cmd)
            response = (self.ser.readline())
            # time.sleep(sleeptime[1])
            # print(response)
        else:
            self.ser.write(cmd)
            response = (self.ser.readline())
            print('Gimbal moveing wait', end="...")
            sys.stdout.flush()
            # time.sleep(sleeptime[0])
            print('Done', end="\n==========================\n")
        self.sleep[0] = False
        self.ser.close()
        return response

    @staticmethod
    def f2b(fn):
        return struct.pack("f", fn)

    @staticmethod
    def crc_accumulate(byte, crc_tmp):
        tmp = (byte ^ (crc_tmp & 0xff)) & 0xff
        tmp = (tmp ^ (tmp << 4)) & 0xff
        crc_tmp = ((crc_tmp >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xffff
        return crc_tmp

    def get_crc(self, byte_str):
        crc_tmp = 0xffff
        for b in byte_str:
            crc_tmp = self.crc_accumulate(b, crc_tmp)
        # return crc_tmp
        # return struct.pack('>I', 0xffff & crc_tmp)[:2]
        return struct.pack('I', 0xffff & crc_tmp)[:2]

    def get_version_str(self):
        cmd = bytes.fromhex('FA0002' + self.crc)
        self.cmd_execute(cmd)

    def home_all(self):
        self.set_pitch_roll_yaw(0, 0, 0)

    def home_pitch(self):
        self.setpitch(0)

    def home_roll(self):
        self.setpitch(0)

    def home_yaw(self):
        self.setyaw(0)

    def set_pitch(self, pitch_in):
        pitch = self.converter(pitch_in, 0)
        cmd = bytes.fromhex('FA020A' + pitch + self.crc)
        self.cmd_execute(cmd)

    def set_roll(self, roll_in):
        roll = self.converter(roll_in, 2)
        cmd = bytes.fromhex('FA020B' + roll + self.crc)
        self.cmd_execute(cmd)

    def set_yaw(self, yaw_in):
        yaw = self.converter(yaw_in, 4)
        cmd = bytes.fromhex('FA020C' + yaw + self.crc)
        self.cmd_execute(cmd)

    def set_pitch_roll_yaw(self, pitch_in, roll_in, yaw_in):
        pitch = self.converter(pitch_in, 0)
        yaw = self.converter(roll_in, 2)
        roll = self.converter(yaw_in, 4)
        # 0xFA 0x06 0x12
        cmd = bytes.fromhex('FA0612' + pitch + roll + yaw + self.crc)
        self.cmd_execute(cmd)

    def set_angle(self, pitch, roll, yaw):
        # 0xFA 0x0E 0x11
        # float1 float2 float3 flags-byte type-byte crc-low-byte crc-high-byte
        out = b'\x0e\x11' + self.f2b(pitch) + self.f2b(roll) + self.f2b(yaw) + b'\x00\x00'
        out = b'\xfa' + out + bytes.fromhex(self.crc)
        self.cmd_execute(out)

    '''
    Checks input to see if it's in-bounds
    :param input: specific angle value
    :param axis: on which axis has to be applied
    :return: applicable input value 
    '''

    def axis_check(self, angle, axis):

        if angle < self.axis_limit[axis]:
            angle = self.axis_limit[axis]
            print(f'{axis} exceeds min travel parameter! ')
            print('Input was adjusted to max travel distance.')
        elif angle > self.axis_limit[(axis + 1)]:
            angle = self.axis_limit[(axis + 1)]
            print(f'{axis} exceeds max travel parameter! ')
            print('Input was adjusted to max travel distance.')
        return angle

    '''
    converts input to usable HEX data
    '''

    def converter(self, angle, axis):
        value = self.axis_check(angle, axis)
        sleep_input = abs(value - self.axis_pos[0])
        if value <= self.zero_point[0]:
            # Converts user input to movement distance
            raw = int(1500 + (self.dof_interval[0] * value))
        else:
            raw = int(1500 + (self.dof_interval[1] * value))
        # Re-orders bytes to Low-High in pairs of two
        angle = decto(raw)
        # print(pitch)
        self.sleep_time[0] = ((self.sleep_multiplier[0] * sleep_input) + self.sleep_multiplier[1])
        self.axis_pos[0] = value
        self.sleep[0] = True
        print('{}:', value, end='°\n')
        return angle


def main():
    sys.stdout.flush()
    ctrl_unit = ControlUnit(**settings)
    print('Initializing...', end='')

    safe_mode = ctrl_unit.response_test(ctrl_unit.ser)
    ctrl_unit.param_store(safe_mode)
    ctrl_unit.sleep_multiplier_calc()
    ctrl_unit.interval_calc()
    print("Done")
    ctrl_unit.data_log(safe_mode)
    
    ctrl_unit.set_pitch(0)


if __name__ == '__main__':
    main()
