import numpy as np
import os


with np.load(os.getcwd() + '/data.npz') as file:
    _, mtx, dist, r_m, t_m = [file[i] for i in ('ret', 'mtx', 'dist', 'rotation', 'translation')]
    print(f"Intrinsic matrix:{mtx}")


for i in dist:
    print(np.around(i, 3))