import matplotlib.pyplot as plt
import numpy as np


# Similation parameters
Kp = 15
dt = 0.01

# Link lengths
l1 = l2 = 1

# Set initial goal position to the initial end-effector position
x = 2
y = 0

show_animation = True

if show_animation:
    plt.ion()


def two_joint_arm(GOAL_TH=0.0, theta1=0.0, theta2=0.0):
    """
    Computes the inverse kinematics for a planar 2DOF arm
    When out of bounds, rewrite x and y with last correct values
    """
    global x, y
    while True:
        try:
            if x is not None and y is not None:
                x_prev = x
                y_prev = y
            if np.sqrt(x**2 + y**2) > (l1 + l2):
                theta2_goal = 0
            else:
                theta2_goal = np.arccos(
                    (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2))
                theta1_goal = np.math.atan2(
                    y, x) - np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))

            if theta1_goal < 0:
                theta2_goal = -theta2_goal
                theta1_goal = np.math.atan2(
                    y, x) - np.math.atan2(l2 * np.sin(theta2_goal), (l1 + l2 * np.cos(theta2_goal)))

            theta1 = theta1 + Kp * ang_diff(theta1_goal, theta1) * dt
            theta2 = theta2 + Kp * ang_diff(theta2_goal, theta2) * dt
        except ValueError as e:
            print("Unreachable goal")
        except TypeError:
            x = x_prev
            y = y_prev

        wrist = plot_arm(theta1, theta2, x, y)

        # check goal
        if x is not None and y is not None:
            d2goal = np.hypot(wrist[0] - x, wrist[1] - y)

        if abs(d2goal) < GOAL_TH and x is not None:
            return theta1, theta2


def plot_arm(theta1, theta2, x, y):  # pragma: no cover
    shoulder = np.array([0, 0])
    elbow = shoulder + np.array([l1 * np.cos(theta1), l1 * np.sin(theta1)])
    wrist = elbow + \
        np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2)])

    if show_animation:
        plt.cla()

        plt.plot([shoulder[0], elbow[0]], [shoulder[1], elbow[1]], 'k-')
        plt.plot([elbow[0], wrist[0]], [elbow[1], wrist[1]], 'k-')

        plt.plot(shoulder[0], shoulder[1], 'ro')
        plt.plot(elbow[0], elbow[1], 'ro')
        plt.plot(wrist[0], wrist[1], 'ro')

        plt.plot([wrist[0], x], [wrist[1], y], 'g--')
        plt.plot(x, y, 'g*')

        plt.xlim(-2, 2)
        plt.ylim(-2, 2)

        plt.show()
        plt.pause(dt)

    return wrist


def ang_diff(theta1, theta2):
    # Returns the difference between two angles in the range -pi to +pi
    return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi


def click(event):  # pragma: no cover
    global x, y
    x = event.xdata
    y = event.ydata


if __name__ == "__main__":
    fig = plt.figure()
    fig.canvas.mpl_connect("button_press_event", click)
    # for stopping simulation with the esc key.
    fig.canvas.mpl_connect('key_release_event', lambda event: [
                           exit(0) if event.key == 'escape' else None])
    two_joint_arm()
