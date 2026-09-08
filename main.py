

import cv2
import numpy as np
import time

# -----------------------------
# Configuration
# -----------------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
BACKGROUND_SAMPLES = 24
COUNTDOWN_SECONDS = 5

# Blue segmentation defaults. Tune these if your cloth/lighting differs.
LOWER_BLUE = np.array([90, 65, 35], dtype=np.uint8)
UPPER_BLUE = np.array([140, 255, 255], dtype=np.uint8)

MIN_COMPONENT_AREA = 350
MORPH_KERNEL_SIZE = 5
FEATHER_SIZE = 7
MASK_SMOOTHING = 0.45

WINDOW_NAME = "Invisible Cloak AI Pro | ESC/Q: Exit | R: Recapture | C: Calibrate"


def open_camera():
    """Open webcam with a Windows-friendly backend when available."""
    if hasattr(cv2, "CAP_DSHOW"):
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    return cap


def configure_camera(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    # Small camera buffer reduces visible delay on many webcams.
    try:
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    except Exception:
        pass


def read_frame(cap):
    ret, frame = cap.read()
    if not ret or frame is None:
        return None
    return cv2.flip(frame, 1)


def capture_background(cap, samples=BACKGROUND_SAMPLES):
    """Capture several clean frames and use their median to reduce noise."""
    frames = []
    for _ in range(samples):
        frame = read_frame(cap)
        if frame is not None:
            # A small resize keeps memory reasonable on high-resolution webcams.
            frames.append(frame)
        time.sleep(0.035)

    if not frames:
        return None

    stack = np.stack(frames, axis=0)
    background = np.median(stack, axis=0).astype(np.uint8)
    return background


def countdown(cap, seconds=COUNTDOWN_SECONDS):
    """Show a visual countdown before background capture."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        frame = read_frame(cap)
        if frame is None:
            return False

        remaining = max(1, int(np.ceil(end_time - time.time())))
        draw_panel(frame, "STEP 1  |  MOVE OUT OF FRAME", f"Background capture in {remaining}")
        cv2.putText(
            frame, str(remaining), (frame.shape[1] // 2 - 30, frame.shape[0] // 2),
            cv2.FONT_HERSHEY_SIMPLEX, 3.0, (255, 255, 255), 7, cv2.LINE_AA
        )
        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            return False
    return True


def make_mask(frame, lower_blue, upper_blue):
    """Create a robust blue-cloth mask and remove small noisy components."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Morphological cleanup closes tiny holes and removes isolated noise.
    k = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (MORPH_KERNEL_SIZE, MORPH_KERNEL_SIZE)
    )
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)

    # Keep meaningful connected regions only.
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    cleaned = np.zeros_like(mask)
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if area >= MIN_COMPONENT_AREA:
            cleaned[labels == label] = 255

    # Fill small holes and soften jagged edges.
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, k, iterations=1)
    return cleaned


def calibrate_from_center(frame):
    """Estimate blue HSV limits from a center ROI containing the cloak."""
    h, w = frame.shape[:2]
    x1, x2 = int(w * 0.35), int(w * 0.65)
    y1, y2 = int(h * 0.25), int(h * 0.75)
    roi = frame[y1:y2, x1:x2]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Use only pixels that are already reasonably saturated/visible.
    valid = hsv[(hsv[:, :, 1] > 45) & (hsv[:, :, 2] > 30)]
    if len(valid) < 100:
        return None

    # Robust percentiles avoid one or two extreme pixels dominating calibration.
    h_low, h_high = np.percentile(valid[:, 0], [5, 95])
    s_low = np.percentile(valid[:, 1], 10)
    v_low = np.percentile(valid[:, 2], 10)

    # A generous hue margin helps with folds and shadows.
    low_h = max(0, int(h_low) - 8)
    high_h = min(179, int(h_high) + 8)
    low_s = max(35, int(s_low) - 25)
    low_v = max(25, int(v_low) - 25)

    return (
        np.array([low_h, low_s, low_v], dtype=np.uint8),
        np.array([high_h, 255, 255], dtype=np.uint8),
    )


def feather_mask(mask):
    size = FEATHER_SIZE if FEATHER_SIZE % 2 == 1 else FEATHER_SIZE + 1
    return cv2.GaussianBlur(mask, (size, size), 0)


def create_cloak_effect(frame, background, mask, previous_mask=None):
    """Replace the masked cloak area with the captured background."""
    if previous_mask is not None:
        mask = cv2.addWeighted(mask, MASK_SMOOTHING, previous_mask, 1.0 - MASK_SMOOTHING, 0)

    soft = feather_mask(mask)
    alpha = soft.astype(np.float32) / 255.0
    alpha = alpha[:, :, None]

    result = (
        frame.astype(np.float32) * (1.0 - alpha)
        + background.astype(np.float32) * alpha
    ).clip(0, 255).astype(np.uint8)

    return result, mask


def draw_panel(frame, title, subtitle, fps=None, coverage=None):
    """Draw a clean information panel on the preview."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (15, 15), (535, 132), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)

    cv2.putText(frame, title, (30, 48), cv2.FONT_HERSHEY_SIMPLEX,
                0.72, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, subtitle, (30, 78), cv2.FONT_HERSHEY_SIMPLEX,
                0.56, (225, 225, 225), 1, cv2.LINE_AA)

    if fps is not None:
        cv2.putText(frame, f"FPS: {fps:5.1f}", (30, 108),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (220, 220, 220), 1, cv2.LINE_AA)
    if coverage is not None:
        cv2.putText(frame, f"Cloak mask: {coverage:4.1f}%", (160, 108),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (220, 220, 220), 1, cv2.LINE_AA)


def draw_calibration_roi(frame):
    h, w = frame.shape[:2]
    x1, x2 = int(w * 0.35), int(w * 0.65)
    y1, y2 = int(h * 0.25), int(h * 0.75)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
    cv2.putText(frame, "Place BLUE CLOTH here", (x1, y1 - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)


def main():
    print("=" * 64)
    print("  INVISIBLE CLOAK AI PRO - Python + OpenCV")
    print("=" * 64)
    print("Starting camera...")

    cap = open_camera()
    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        print("Try changing CAMERA_INDEX from 0 to 1 in main.py.")
        return

    configure_camera(cap)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1100, 700)

    # Let the webcam exposure settle.
    for _ in range(20):
        read_frame(cap)
        cv2.waitKey(1)

    if not countdown(cap):
        cap.release()
        cv2.destroyAllWindows()
        return

    print("Capturing clean background...")
    background = capture_background(cap)
    if background is None:
        print("ERROR: Background capture failed.")
        cap.release()
        cv2.destroyAllWindows()
        return

    print("Background captured successfully.")
    print("Enter the frame wearing the BLUE cloak.")
    print("Optional: press C while the blue cloth is inside the calibration box.")
    print("Press R to recapture the background; Q or ESC to exit.")

    lower_blue = LOWER_BLUE.copy()
    upper_blue = UPPER_BLUE.copy()
    previous_mask = None
    last_time = time.time()
    fps = 0.0

    while True:
        frame = read_frame(cap)
        if frame is None:
            print("WARNING: Camera frame could not be read.")
            break

        mask = make_mask(frame, lower_blue, upper_blue)
        result, previous_mask = create_cloak_effect(
            frame, background, mask, previous_mask
        )

        now = time.time()
        dt = max(now - last_time, 1e-6)
        instant_fps = 1.0 / dt
        fps = instant_fps if fps == 0 else (fps * 0.9 + instant_fps * 0.1)
        last_time = now

        coverage = 100.0 * float(np.count_nonzero(mask)) / float(mask.size)
        draw_panel(
            result,
            "INVISIBLE CLOAK AI PRO",
            "Blue cloth detected → matching background restored",
            fps,
            coverage,
        )

        cv2.imshow(WINDOW_NAME, result)

        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            break

        if key in (ord("r"), ord("R")):
            print("Recapturing background... move completely out of frame.")
            if countdown(cap):
                new_background = capture_background(cap)
                if new_background is not None:
                    background = new_background
                    previous_mask = None
                    print("Background recaptured.")
            else:
                break

        if key in (ord("c"), ord("C")):
            calibrated = calibrate_from_center(frame)
            if calibrated is None:
                print("Calibration failed: place the BLUE cloth inside the box.")
            else:
                lower_blue, upper_blue = calibrated
                previous_mask = None
                print(
                    "Calibration updated: "
                    f"HSV lower={lower_blue.tolist()}, upper={upper_blue.tolist()}"
                )

    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed. Project finished.")


if __name__ == "__main__":
    main()
