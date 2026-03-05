import numpy as np
from scipy.ndimage import center_of_mass

def refine_subpixel(gray_roi):
    roi_float = gray_roi.astype(np.float32)
    cy, cx = center_of_mass(roi_float)
    return float(cx), float(cy)
