Object Tracking Using Sub-Pixel

This project implements an object tracking system using computer vision techniques with Python and OpenCV. The system tracks objects in video frames with improved accuracy using sub-pixel refinement.

Requirements

Before running the project, make sure the following software is installed on your system:

Python 3.10 or later

pip (Python package manager)

Git (optional, for cloning the repository)

Step 1: Clone or Download the Project

You can download the project as a ZIP file or clone it using Git.

Using Git:

git clone [https://github.com/your-username/Object-Tracking-Using-Sub-Pixel.git](https://github.com/Rabin20/Object-Tracking-Using-Sub-Pixel.git)

Then move into the project folder:

cd Object-Tracking-Using-Sub-Pixel

If you downloaded the ZIP file, extract it and open the folder in your terminal.

Step 2: Create a Virtual Environment

Creating a virtual environment keeps project dependencies separate from your system Python.

Run:

python -m venv venv

This will create a folder named venv.

Step 3: Activate the Virtual Environment
Windows (PowerShell)
venv\Scripts\activate
Mac/Linux
source venv/bin/activate

After activation you should see:

(venv)

in your terminal.

Step 4: Install Required Packages

Install all required dependencies using:

pip install -r requirements.txt

This will install libraries such as:

numpy

opencv-python

Step 5: Run the Project

Once the installation is complete, run the main program:

python src/main.py

The program will start the object tracking process.
