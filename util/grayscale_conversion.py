import cv2
import numpy as np


def grayscale_conversion(image):
    gray_image = np.zeros_like(image)
    gray_image[:, :, 0] = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image[:, :, 1] = gray_image[:, :, 0]
    gray_image[:, :, 2] = gray_image[:, :, 0]

    return gray_image
