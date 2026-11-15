# Camera detection and garment sorting

## Camera preview

The first stage checks that Python and OpenCV can open a camera and display its
live video. It does not assume a camera model, image resolution, robot
dimensions, or ROS 2 topics.

Install OpenCV:

```bash
python -m pip install opencv-python
```

Run from the repository root:

```bash
python camera_detection/camera_test.py
python camera_detection/camera_test.py --camera 1
```

Camera index `0` is only a starting point. Press **q** in the preview window to
close it. The program releases the camera when it exits.

## Garment sorter orchestration module

`camera_detection/garment_sorter.py` separates the sorting workflow from the
camera test. It provides `run_sorting_loop()` and a `GarmentSorterHardware`
protocol for future vision and robot adapters. Its control flow covers garment
detection, grasp-point estimation, pickup verification, lifting, color-based
routing, and an uncertain-color destination.

This is orchestration scaffolding, not a complete robot controller. It does not
implement a detector, classifier, camera calibration, arm driver, gripper
control, or ROS 2 integration. A hardware adapter must implement those
operations and enforce workspace bounds, collision checks, speed/force limits,
emergency-stop handling, and safe recovery behavior. Start with mocked or
dry-run adapters; do not connect actuator movement until safety checks and
calibration have been independently validated.

The loop is bounded by `max_cycles` (default `100`) so a faulty
`garments_remaining()` signal or repeated detection failure cannot cause an
unbounded run. The adapter's `retry_grasp()` should perform only a safe,
bounded recovery; the workflow then starts the next cycle.

## Recommended project development schedule

### Phase 1 — Machine vision on the MacBook

- Open and test the iPhone camera feed through a supported camera connection.
- Learn image capture with OpenCV and save representative test images.
- Evaluate a garment detector (for example, YOLO) on those images.
- Develop DARK/LIGHT classification and include an uncertain result for
  ambiguous cases.
- Test with real laundry under varied lighting and backgrounds.

**Exit check:** repeatable camera capture and documented detection/classification
results on a held-out set of laundry images. Do not treat an iPhone as a camera
source until its feed is available to the Mac as a camera device or stream.

### Phase 2 — Garment segmentation and grasp detection

- Train or adapt a garment segmentation model.
- Identify fabric regions, edges, and candidate grasp points.
- Estimate grasp position in the camera coordinate frame and quantify
  uncertainty.
- Test across fabric types, folds, occlusion, and lighting.

**Exit check:** stable grasp candidates with confidence/uncertainty measurements;
no robot motion is needed in this phase.

### Phase 3 — Camera and robotic-arm integration

- Configure the wrist camera and calibrate camera-to-gripper coordinates.
- Add a hardware adapter implementing `GarmentSorterHardware`.
- Test arm poses and pickup verification first in simulation or a guarded,
  low-speed setup.
- Validate workspace limits, emergency stop, collision handling, and recovery
  before attempting repeated picks.

**Exit check:** measured calibration error and repeatable, supervised grasp/lift
trials.

### Phase 4 — JetAuto integration

- Integrate mobile navigation only after arm and perception tests are reliable.
- Locate scattered garments and coordinate the mobile base with the arm.
- Define safe drop-off poses and deliver garments to the basins.

**Exit check:** supervised end-to-end trials with the base stationary first,
followed by controlled navigation tests.

### Phase 5 — Full-system testing

- Test multiple scattered garments and edge cases, including failed detections
  and failed grasps.
- Measure classification accuracy, grasp success rate, sorting accuracy, and
  cycle time.
- Record failures and repeat tests across representative conditions.

**Exit check:** meet project-defined safety and performance thresholds before
unattended operation. Keep emergency-stop access available during testing.
