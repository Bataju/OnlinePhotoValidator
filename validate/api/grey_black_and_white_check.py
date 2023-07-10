def is_grey(img):
    w, h, channel = img.shape
    for i in range(w):
        for j in range(h):
            r, g, b = img[i][j]

            if abs(int(r)-int(g)) > 26 or abs(int(r)-int(g)) > 26 or abs(int(r)-int(g)) > 26:
                return False
    return True