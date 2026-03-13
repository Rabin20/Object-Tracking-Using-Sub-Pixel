import numpy as np

class DriftCorrector:
    def __init__(self):
        self.history = []

    def update(self, displacement):
        self.history.append(displacement)
        if len(self.history) > 10:
            self.history.pop(0)

    def corrected(self, displacement):
        bias = np.mean(self.history) if self.history else 0
        return displacement - bias
