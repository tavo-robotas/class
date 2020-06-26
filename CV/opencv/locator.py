

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

