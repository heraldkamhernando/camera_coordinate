# Camera detection: first test

This first stage checks that Python and OpenCV can open a camera and display
its live video. It does not make assumptions about the camera model, image
resolution, robot dimensions, or ROS 2 topics.

## Requirements

- Python 3
- A camera connected to the computer running this script
- OpenCV's Python package

Install OpenCV from VS Code Terminal:

```bash
python -m pip install opencv-python
```

On some systems, the Python command is `python3` instead of `python`.

## Run the camera preview

From the repository root in VS Code Terminal:

```bash
python camera_detection/camera_test.py
```

The script starts with camera index `0` as a common starting point, not as a
claim about which device is connected. If it cannot open that device, try
another index, for example:

```bash
python camera_detection/camera_test.py --camera 1
```

Press **q** while the preview window is active to close it. The program
releases the camera when it exits.

## Expected result

A window titled **Camera Preview - press q to quit** shows live frames. If the
camera cannot be opened or frames cannot be read, the terminal prints a
troubleshooting message instead of proceeding to coordinate processing.

## Next step

Run this test and share the terminal output, whether a preview appeared, your
operating system, and the camera make/model or type if known. Do not proceed to
coordinate or robot movement testing until the camera and later calibration
results have been verified.
