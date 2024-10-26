import random
import numpy as np
from PIL import Image

def kn_encrypt(k, n, im):
    im_width, im_height, channel = im.shape

    recons = n - k + 1
    img_share = np.zeros((n, im_width, im_height, channel*8), dtype=np.uint8)

    for i in range(im_width):
        for j in range(im_height):
            PIX = np.concatenate([np.unpackbits(im[i, j, :], axis=-1)], axis=-1)
            for l in range(24):
                if PIX[l] == 1:
                    temp = random.sample(range(n), recons)
                    for t in temp:
                        img_share[t, i, j, l] = 1

    for i in range(n):
        red_share = np.packbits(img_share[i, :, :, :8], axis=-1)
        green_share = np.packbits(img_share[i, :, :, 8:16], axis=-1)
        blue_share = np.packbits(img_share[i, :, :, 16:], axis=-1)

        ith_share = np.concatenate([red_share, green_share, blue_share], axis=-1)
        ith_share = Image.fromarray(ith_share, mode='RGB')
        ith_share.save(f'share{i+1}.png')

# Load input image
im = np.array(Image.open('op2.png'), dtype=np.uint8)

# Perform k-n secret sharing
k = 3
n = 6
kn_encrypt(k, n, im)
