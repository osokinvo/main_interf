import colour
import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

color_mf = colour.colorimetry.MSDS_CMFS_RGB['Wright & Guild 1931 2 Degree RGB CMFs']
weiw = color_mf.wavelengths
mf = color_mf.values
def interf(lambda1, r1, r2, d, n=1.7):
    if r2 > 10 - r1:
        r2 = 10 - r1
        a = r2*np.cos(4*np.pi*n*d/lambda1)
    return abs(r1 + a)

d_max = 1500
k = [d for d in range(d_max)]
k_s = np.array([k] * len(weiw))
weiw_f = np.array([weiw]*d_max)
print(weiw_f.shape)
for r1 in range(1,10):
    r2 = 10-r1
    s_1050 = [[interf(lam, r1, r2, d) for lam in weiw] \
        for d in k]
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    # print(lens_1050.shape)
    s = np.array(s_1050)
    print(s.shape, len(k), len(weiw), s.max())
    ax.plot_surface(weiw_f,k_s.T, s, cmap = cm.plasma)
    img = s.dot(np.array(mf))
    img1 = img/73.0303
    print(img.max())
    img2 = np.zeros((100, d_max, 3))
    img2[:] = img1
    cv.imwrite(f'img_{r1}_{r2}.bmp',img2 * 255)