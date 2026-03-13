from ultralytics import YOLO

class YOLODetector:

    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(frame)

        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()

            if len(boxes) > 0:
                x1,y1,x2,y2 = boxes[0]
                w = x2 - x1
                h = y2 - y1

                return (int(x1), int(y1), int(w), int(h))

        return None