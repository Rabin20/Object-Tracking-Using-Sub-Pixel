# Object Tracking Using Sub-Pixel (Web App Version)

This project implements a highly accurate object tracking system utilizing Python, OpenCV, and Flask. The system tracks objects in video frames with improved accuracy using **sub-pixel refinement** and streams the live results directly to a **Web Browser Interface**.

## Features

- **Web-Based Interface**: Built on Flask, removing the need for local OpenCV window GUIs. 
- **Interactive ROI Selection**: If the YOLO automated detection fails, you can manually select the tracking target by simply clicking and dragging a bounding box over the video directly within your web browser.
- **Sub-Pixel Refinement**: Uses `scipy.ndimage.center_of_mass` to calculate the exact light intensity centroid of the object, achieving extreme sub-pixel precision.
- **Drift Correction Engine**: Automatically plots the sub-pixel motion curve and saves it upon completion.
- **Responsive Video Feed**: Live MJPEG streaming to dynamically resized viewports.

## Requirements

Before running the project, make sure the following software is installed on your system:
- **Python 3.10** or later
- **pip** (Python package manager)
- **Git** (optional, for cloning the repository)

## Step 1: Clone or Download the Project

You can download the project as a ZIP file or clone it using Git.

```bash
git clone https://github.com/Rabin20/Object-Tracking-Using-Sub-Pixel.git
cd Object-Tracking-Using-Sub-Pixel
```

## Step 2: Create a Virtual Environment

Creating a virtual environment keeps project dependencies separate from your system Python.

```bash
python -m venv venv
```

## Step 3: Activate the Virtual Environment

**Windows (PowerShell)**:
```powershell
venv\Scripts\activate
```

**Mac/Linux**:
```bash
source venv/bin/activate
```

*(You should see `(venv)` in your terminal prompt after activation.)*

## Step 4: Install Required Packages

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

This will install libraries such as Flask, Flask-Cors, OpenCV, YOLO (Ultralytics), SciPy, and Matplotlib.

## Step 5: Run the Project

Since this is now a Web Application, we start the Flask server instead of the raw Python script:

```bash
python app.py
```

1. Open your web browser and go to `http://127.0.0.1:5000`.
2. The browser will attempt to autodetect the target via YOLO.
3. If YOLO is unable to find the target object, the video will pause with instructions.
4. **Click and drag** a rectangle over the object you wish to track.
5. Tracking will automatically commence!

## Step 6: View the Results

Once the video finishes streaming, the stream will display **"Tracking Finished!"**. 
The system runs the displacement logic silently in the background and saves a high-quality Matplotlib graph to:
- `src/output/plots/displacement.png`
