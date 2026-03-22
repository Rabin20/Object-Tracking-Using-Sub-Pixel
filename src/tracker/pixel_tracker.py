import cv2

class PixelTracker:
    def __init__(self, bbox):
        # Initialize CSRT tracker
        self.tracker = cv2.TrackerCSRT_create()
        self.bbox = bbox

    def init(self, frame):
        """Initialize tracker with first frame."""
        self.tracker.init(frame, self.bbox)

    def update(self, frame):
        """Update tracker and return new bounding box."""
        success, new_bbox = self.tracker.update(frame)
        return success, new_bbox

    def reinit(self, frame, new_bbox):
        """Recreate and reinitialize tracker with a refined bounding box to prevent drift."""
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, new_bbox)
        self.bbox = new_bbox
