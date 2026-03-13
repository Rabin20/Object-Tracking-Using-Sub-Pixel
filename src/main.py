import cv2
import numpy as np

from data.load_frames import load_image_sequence
from tracker.pixel_tracker import PixelTracker
from tracker.subpixel_refinement import refine_subpixel
from tracker.drift_correction import DriftCorrector
from tracker.roi_update import update_roi
from evaluation.plot_results import plot_displacement_curve
from detector import YOLODetector


def main():

    frames = load_image_sequence("D:/project/mouse-1/img")

    if len(frames) == 0:
        print("No frames loaded")
        return

    first_frame = frames[0]

    # Initialize YOLO detector
    detector = YOLODetector()

    # Try automatic detection
    bbox = detector.detect(first_frame)

    # Fallback to manual ROI if detection fails
    if bbox is None:
        print("YOLO could not detect object. Please select ROI manually.")
        bbox = cv2.selectROI("Select Target", first_frame, False)
        cv2.destroyAllWindows()
    else:
        print("YOLO detected object:", bbox)

    # Initialize tracker
    pixel_tracker = PixelTracker(bbox)
    pixel_tracker.init(first_frame)

    drift = DriftCorrector()
    displacements = []

    for idx, frame in enumerate(frames):

        success, bbox = pixel_tracker.update(frame)

        if not success:
            continue

        x, y, w, h = map(int, bbox)

        # Prevent ROI going outside frame
        h_frame, w_frame = frame.shape[:2]

        x = max(0, x)
        y = max(0, y)
        w = min(w, w_frame - x)
        h = min(h, h_frame - y)

        roi = frame[y:y+h, x:x+w]

        if roi.size == 0:
            continue

        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Subpixel refinement
        cx, cy = refine_subpixel(gray_roi)

        displacement = np.sqrt(cx**2 + cy**2)

        drift.update(displacement)

        corrected = drift.corrected(displacement)

        displacements.append(corrected)

        # Update ROI based on refined center
        new_bbox = update_roi(bbox, cx, cy)

        pixel_tracker.bbox = new_bbox

        # Draw bounding box
        cv2.rectangle(frame,
                      (new_bbox[0], new_bbox[1]),
                      (new_bbox[0] + new_bbox[2],
                       new_bbox[1] + new_bbox[3]),
                      (0, 255, 0), 2)

        cv2.putText(frame,
                    f"Subpixel: {corrected:.3f}",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2)

        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) == 27:
            break

    # Save displacement plot
    plot_displacement_curve(
        displacements,
        "src/output/plots/displacement.png"
    )

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()