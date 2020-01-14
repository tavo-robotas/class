import cv2
import numpy as np
import imutils
import time
import pyrealsense2 as rs
import pickle
import socket

def call(x):
    pass


cv2.namedWindow('sense', cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('LH', 'sense', 0, 255, call)
cv2.createTrackbar('LS', 'sense', 0, 255, call)
cv2.createTrackbar('LV', 'sense', 0, 255, call)
cv2.createTrackbar('UH', 'sense', 255, 255, call)
cv2.createTrackbar('US', 'sense', 255, 255, call)
cv2.createTrackbar('UV', 'sense', 255, 255, call)


pipe = rs.pipeline()
configure = rs.config()
configure.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipe.start(configure)

header_size = 10

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((socket.gethostname(), 4400))
soc.listen(5)


try:
    while pipe:
        frames = pipe.wait_for_frames()

        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        else:
            color_image = np.asanyarray(color_frame.get_data())
            blurred = cv2.GaussianBlur(color_image, (13, 13), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            l_h = cv2.getTrackbarPos('LH', 'sense')
            l_s = cv2.getTrackbarPos('LS', 'sense')
            l_v = cv2.getTrackbarPos('LV', 'sense')
            u_h = cv2.getTrackbarPos('UH', 'sense')
            u_s = cv2.getTrackbarPos('US', 'sense')
            u_v = cv2.getTrackbarPos('UV', 'sense')

            lower_bound = np.array([l_h, l_s, l_v])
            upper_bound = np.array([u_h, u_s, u_v])

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            # cv erode documentation
            mask = cv2.erode(mask, None, iterations=2)
            # cv dilate documentation
            mask = cv2.dilate(mask, None, iterations=2)

            result = cv2.bitwise_and(color_image, color_image, mask=mask)

            outlines = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(outlines)
            if len(contours) > 0:
                # print(contours)
                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

                if radius > 10:

                    cv2.circle(color_image, (int(x), int(y)),
                               int(radius), (0, 255, 255), 2)
                    cv2.circle(color_image, center, 5, (255, 255, 255), -1)
                    coordinates = str(int(x)) + ' : ' + str(int(y))
                    image = cv2.putText(
                        color_image,
                        coordinates,
                        (30, 40),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA)
                    # msg = center
                    # msg = f'{len(msg):<{header_size}}' + msg
                    # client.send(bytes(msg, 'utf-8'))

                #cv2.drawContours(image, contours, -1, (0, 255, 255), 3)

            cv2.imshow('image', color_image)
            cv2.imshow('mask', mask)
            cv2.imshow('rest', result)

            key = cv2.waitKey(1)
            if key == 27:
                break
finally:
    # Stop streaming
    pipe.stop()
