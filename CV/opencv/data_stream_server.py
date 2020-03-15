#!/usr/bin/python
import pyrealsense2 as rs
import sys
import imutils
import asyncore
import numpy as np
import pickle
import socket
import struct
import cv2
import pdb

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
mc_ip_address = socket.gethostname()
print(mc_ip_address)
port = 1024
chunk_size = 4096

# rs.log_to_console(rs.log_severity.debug)

def getFrame(pipeline, processing):
    frames = pipeline.wait_for_frames()
    # take owner ship of the frame for further processing
    frames.keep()
    depth = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if color_frame:
        frame = processing.process(color_frame)
        # take owner ship of the frame for further processing
        frame.keep()
        # represent the frame as a numpy array
        data = frame.as_frame().get_data()
        color_image = np.asanyarray(data)

        blurred = cv2.GaussianBlur(color_image, (13, 13), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        l_h = 30
        l_s = 180
        l_v = 50
        u_h = 255
        u_s = 255
        u_v = 150

        l_bound = np.array([l_h, l_s, l_v])
        u_bound = np.array([u_h, u_s, u_v])
        low_thr = np.array(l_bound)
        upp_thr = np.array(u_bound)

        mask = cv2.inRange(hsv, low_thr, upp_thr)
        # cv erode documentation
        mask = cv2.erode(mask, None, iterations=2)
        # cv dilate documentation
        mask = cv2.dilate(mask, None, iterations=2)

        # result = cv2.bitwise_and(color_image, color_image, mask=mask)
        outlines = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(outlines)
        rectangle = cv2.minAreaRect(contours)

        (x, y), (w, h), a = rectangle

        if len(contours) > 0:
            raw = np.asanyarray('s', 'generic', x, y, a, 'e')
            return raw

            # for contour in contours:
            # (x, y, w, h) = cv2.boundingRect(contour)
            # # print(contours)
            # c = max(contours, key=cv2.contourArea)
            # ((x, y), radius) = cv2.minEnclosingCircle(c)
            # M = cv2.moments(c)
            # center = (round(float(M['m10'] / M['m00']), 2), round(float(M['m01'] / M['m00']), 2))
            # if radius > 10:
            #     raw = np.asanyarray(center)
            #     return raw



    else:
        return None


def openPipeline():
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline = rs.pipeline()
    pipeline.start(cfg)
    return pipeline


class DevNullHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        print(self.recv(1024))

    def handle_close(self):
        self.close()


class EtherSenseServer(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        print("Launching Realsense Camera Server")
        try:
            self.pipeline = openPipeline()
        except:
            print("Unexpected error: ", sys.exc_info()[1])
            sys.exit(1)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print('sending acknowledgement to', address)

        # reduce the resolution of the depth image using post processing
        self.filter = rs.decimation_filter()
        self.filter.set_option(rs.option.filter_magnitude, 2)

        self.frame_data = ''
        self.connect((address[0], 1024))
        self.packet_id = 0

    def handle_connect(self):
        print("connection received")

    def writable(self):
        return True

    def update_frame(self):
        frame = getFrame(self.pipeline, self.filter)
        if frame is not None:
            # convert the depth image to a string for broadcast

            data = pickle.dumps(frame)
            pdb.set_trace()
            # capture the length of the data portion of the message
            length = struct.pack('<f', len(data))
            # for the message for transmission
            self.frame_data = b''.join([length, data])

    def handle_write(self):
        # first time the handle_write is called
        if not hasattr(self, 'frame_data'):
            self.update_frame()
        # the frame has been sent in it entirety so get the latest frame
        if len(self.frame_data) == 0:
            self.update_frame()
        else:
            # send the remainder of the frame_data until there is no data remaining for transmition
            remaining_size = self.send(self.frame_data)
            self.frame_data = self.frame_data[remaining_size:]

    def handle_close(self):
        self.close()


class MulticastServer(asyncore.dispatcher):
    def __init__(self, host=mc_ip_address, port=1024):
        asyncore.dispatcher.__init__(self)
        server_address = ('', port)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(server_address)

    def handle_read(self):
        data, addr = self.socket.recvfrom(42)
        print('Recived Multicast message %s bytes from %s' % (data, addr))
        # Once the server recives the multicast signal, open the frame server
        EtherSenseServer(addr)
        print(sys.stderr, data)

    def writable(self):
        return False  # don't want write notifies

    def handle_close(self):
        self.close()

    def handle_accept(self):
        channel, addr = self.accept()
        print('received %s bytes from %s' % (data, addr))


def main(argv):
    # initalise the multicast receiver
    server = MulticastServer()
    # hand over excicution flow to asyncore
    asyncore.loop()


if __name__ == '__main__':
    main(sys.argv[1:])
