"""Open a live camera preview with OpenCV.

Usage from the repository root:
    python camera_detection/camera_test.py
    python camera_detection/camera_test.py --camera 1

The default camera index (0) is only a starting point. Select the index that
matches the camera connected to your computer; no camera model is assumed.
"""

import argparse
import sys

try:
    import cv2
except ImportError:
    print(
        "OpenCV is not installed. Install the Python package with: "
        "python -m pip install opencv-python",
        file=sys.stderr,
    )
    raise SystemExit(1)


def main():
    """Open the selected camera, show frames, and release resources on exit."""
    parser = argparse.ArgumentParser(description="Preview a camera using OpenCV")
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="camera device index (default: 0; try another index if needed)",
    )
    args = parser.parse_args()

    camera = cv2.VideoCapture(args.camera)
    if not camera.isOpened():
        print(
            f"Could not open camera index {args.camera}. Check the connection, "
            "permissions, and whether another application is using it. "
            "You can try a different index with --camera N.",
            file=sys.stderr,
        )
        camera.release()
        raise SystemExit(1)

    print(f"Camera index {args.camera} opened. Press q in the preview window to quit.")
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print(
                    "The camera opened, but a frame could not be read. "
                    "Check the connection and camera availability.",
                    file=sys.stderr,
                )
                break

            cv2.imshow("Camera Preview - press q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except cv2.error as error:
        print(f"OpenCV camera/display error: {error}", file=sys.stderr)
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Camera released; preview closed.")


if __name__ == "__main__":
    main()
