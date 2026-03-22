import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, Response, request, jsonify
from main import generate_tracking_frames, set_manual_roi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_roi', methods=['POST'])
def update_roi():
    data = request.json
    bbox = (int(data['x']), int(data['y']), int(data['w']), int(data['h']))
    set_manual_roi(bbox)
    return jsonify({"status": "success", "roi": bbox})

@app.route('/video_feed')
def video_feed():
    return Response(generate_tracking_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
