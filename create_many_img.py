# Подключаем библиотеки
import colour
import cv2 as cv
import numpy as np

# Выбераем параметры стандарта 'Wright & Guild 1931 2 Degree RGB CMFs'
color_mf = colour.colorimetry.MSDS_CMFS_RGB['Wright & Guild 1931 2 Degree RGB CMFs']
# Список длин волн
wl = color_mf.wavelengths
# Список коэффициентов восприимчивости глазом длин волн света
mf = color_mf.values

# Функция интерференции
def interf(wavelength, r1, r2, d, n=1.7):

    if r2 > 10 - r1:
        r2 = 10 - r1
    amplitude = r2*np.cos(4*np.pi*n*d/wavelength)
    return abs(r1 + amplitude)

# Максимальная толщина пленки
d_max = 1500

# Спискок толщин
d_list = [d for d in range(d_max)]

rect_img = np.zeros((100, d_max, 3))
for r1 in range(1,10):
    r2 = 10 - r1
    color_line = [[interf(lam, r1, r2, d) for lam in wl] \
        for d in d_list]
    np_color_line = np.array(color_line)
    img = np_color_line.dot(np.array(mf))
    norm_img = img / img.max()
    rect_img[:] = norm_img
    cv.imwrite(f'img_{r1}_{r2}.bmp', rect_img * 255)