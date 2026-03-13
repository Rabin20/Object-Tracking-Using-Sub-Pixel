import numpy as np
import cv2

def generate_synthetic_motion(image, dx=0.3, dy=0.2):
    transform = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(image, transform, (image.shape[1], image.shape[0]))
