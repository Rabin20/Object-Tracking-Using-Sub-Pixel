import cv2
import numpy as np
import time

from data.load_frames import load_image_sequence

manual_roi = None

def set_manual_roi(bbox):
    global manual_roi
    manual_roi = bbox
from tracker.pixel_tracker import PixelTracker
from tracker.subpixel_refinement import refine_subpixel
from tracker.drift_correction import DriftCorrector
from tracker.roi_update import update_roi
from evaluation.plot_results import plot_displacement_curve
from detector import YOLODetector


def generate_tracking_frames():
    global manual_roi
    manual_roi = None

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
        print("YOLO could not detect object. Waiting for manual ROI from web UI.")
        while manual_roi is None:
            frame_copy = first_frame.copy()
            cv2.putText(frame_copy, "Draw a box to start tracking", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame_copy)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)
            
        bbox = manual_roi
        print("Manual ROI set via web UI:", bbox)
    else:
        print("YOLO detected object:", bbox)

    # Initialize tracker
    pixel_tracker = PixelTracker(bbox)
    pixel_tracker.init(first_frame)

    drift = DriftCorrector()
    displacements = []
    
    # Store the last known manual ROI to detect manual mid-stream corrections
    last_roi = manual_roi

    for idx, frame in enumerate(frames):
        # If the user draws a new box on the web UI, re-initialize the tracker
        if manual_roi != last_roi and manual_roi is not None:
            pixel_tracker = PixelTracker(manual_roi)
            pixel_tracker.init(frame)
            last_roi = manual_roi

        success, bbox = pixel_tracker.update(frame)

        if not success:
            cv2.putText(frame, "Tracking Lost", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
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

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Save displacement plot
    plot_displacement_curve(
        displacements,
        "src/output/plots/displacement.png"
    )

    # Yield a final frame holding the "Tracking Finished" text
    if len(frames) > 0:
        final_frame = frames[-1].copy()
        text = "Tracking Finished!"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (final_frame.shape[1] - text_size[0]) // 2
        text_y = (final_frame.shape[0] + text_size[1]) // 2
        
        cv2.putText(final_frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)
        ret, buffer = cv2.imencode('.jpg', final_frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the final frame a few times to ensure the browser displays it before the connection closes
        for _ in range(5):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.5)

    return

if __name__ == "__main__":
    # If run standalone, we can just iterate the generator but it won't display anything.
    for _ in generate_tracking_frames():
        pass