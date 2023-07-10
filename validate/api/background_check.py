import numpy as np

def background_check(image):
    tolerance_std = 10.00
    h, w, channels = image.shape

    pixels_of_r = []
    pixels_of_g = []
    pixels_of_b = []

    for height in range(0, h):
        for width in range(0, w):
            if (height <= 0.35 * h and (width <= 0.14 * w or width >= 0.86 * w)) or height <= 0.015*h:
                r = image[height, width, 0]
                g = image[height, width, 1]
                b = image[height, width, 2]
                if is_black(r, g, b):
                    return False

                pixels_of_r.append(r)
                pixels_of_g.append(g)
                pixels_of_b.append(b)

    # standard deviation

    std_r = np.std(pixels_of_r)
    std_g = np.std(pixels_of_g)
    std_b = np.std(pixels_of_b)


    # print(std_r)
    # print(std_g)
    # print(std_b)

    return std_r <= tolerance_std and std_g <= tolerance_std and std_b <= tolerance_std


def is_black(r,g,b):
    return r <= 100 and g <= 100 and b <= 100










