import os
import subprocess
import numpy as np
from PIL import Image


def kn_decrypt(shares):
    n, im_width, im_height, channel = shares.shape
    im = np.zeros((im_width, im_height, channel//8), dtype=np.uint8)

    for i in range(im_width):
        for j in range(im_height):
            PIX = np.zeros(24, dtype=np.uint8)
            for l in range(24):
                count = 0
                for k in range(n):
                    if shares[k, i, j, l] == 1:
                        count += 1
                if count >= n - 2:
                    PIX[l] = 1

            red = np.packbits(PIX[:8])
            green = np.packbits(PIX[8:16])
            blue = np.packbits(PIX[16:])
            im[i, j, :] = np.concatenate([red, green, blue], axis=-1)

    return Image.fromarray(im, mode='RGB')




n = 6
shares = np.zeros((n, 512, 512, 24), dtype=np.uint8)
for i in range(n):
    share_image = Image.open(f'share{i+1}.png')
    share_array = np.array(share_image, dtype=np.uint8)
    red_share = np.unpackbits(share_array[:, :, 0], axis=-1)
    green_share = np.unpackbits(share_array[:, :, 1], axis=-1)
    blue_share = np.unpackbits(share_array[:, :, 2], axis=-1)
    pad_height = max(0, 512 - share_array.shape[0])
    pad_width = max(0, 512 - share_array.shape[1])
    shares[i, :, :, :8] = np.pad(red_share, ((0, pad_height), (0, pad_width)), mode='constant')
    shares[i, :, :, 8:16] = np.pad(green_share, ((0, pad_height), (0, pad_width)), mode='constant')
    shares[i, :, :, 16:] = np.pad(blue_share, ((0, pad_height), (0, pad_width)), mode='constant')

# Reconstruct the image using the shares
reconstructed_image = kn_decrypt(shares)
reconstructed_image.save('reconstructed_image.png')
