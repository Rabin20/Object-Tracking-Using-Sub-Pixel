import cv2
import os

def load_image_sequence(folder_path):
    images = []
    for i in range(1, 20000):
        filename = os.path.join(folder_path, f"{i:08}.JPG")
        if not os.path.exists(filename):
            break
        img = cv2.imread(filename)
        if img is None:
            continue
        images.append(img)
    return images
