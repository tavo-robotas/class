import pyrealsense2 as rs
import cv2 as cv
import numpy as np
from evasdk import Eva
import json

xy  = (float, float)
xyz = (float, float, float)

GUESS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
HOME  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
DEEO  = {'w': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0}

class EvaCamera:
    def __init__(self, eva: Eva, crp: xyz, ctop: float):
        self.__eva: eva
        self.__eva_off_pos_x: crp[0]
        self.__eva_off_pos_y: crp[1]
        self.__eva_off_pos_z: crp[2] - ctop

    def move_to_camera(self, cip: xy):
        x, y = xy
        print(f'item x: {x}, item y: {y}')
        eva_relative_x = self.__eva_off_pos_x + x
        eva_relative_y = self.__eva_off_pos_y + y
        eva_relative_z = self.__eva_off_pos_z

        item_pos = {'x': eva_relative_x, 'y': eva_relative_y, 'z': eva_relative_z}

        print(f'move to item position {item_pos}')

        with self.__eva.lock():
            pose = self.__eva.calc_inverse_kinematics(GUESS, item_pos, DEEO)
            self.__eva.control_go_to(pose['ik'][joints])

        print('eva in position')

    def go_home(self):
        print(f'moving home to pose: {HOME}')
        with self.__eva.lock():
            self.__eva.control_go_to(HOME)

        print(f' in {HOME} position')


    def read_from_camera() -> xy:
        return (1.6, 1.1)


    if __name__ == "__main__":
        host = input("eva ip: ")
        token = input("token: ")

        eva = Eva(host, token)
        crp  = (1.2, 2.3, 3.4)
        ctop = 2.2

        ec = EvaCamera(eva, crp, ctop)

        item_position = read_from_camera()

        ec.move_to_camera(item_position)
        ec.go_home()

