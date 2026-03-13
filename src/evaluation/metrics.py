import numpy as np

def displacement_error(gt, pred):
    return np.linalg.norm(np.array(gt) - np.array(pred))

def compute_drift(positions):
    if len(positions) < 2:
        return 0
    return np.linalg.norm(np.array(positions[-1]) - np.array(positions[0]))
