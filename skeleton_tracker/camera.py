import cv2
import os
from threading import Lock

class Camera:
    _instance = None
    _lock = Lock()

    def __new__(cls, camera_index=0):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Camera, cls).__new__(cls)

                # Check if we're in a server environment (no webcam)
                if os.environ.get('DEMO_MODE') or not cls._is_webcam_available(camera_index):
                    print("Running in demo mode with pre-recorded video")
                    # Use demo video instead of webcam
                    video_path = os.path.join(os.path.dirname(__file__), '..', 'demo.mp4')
                    cls._instance.cap = cv2.VideoCapture(video_path)
                    cls._instance.is_demo = True
                else:
                    # Use webcam
                    cls._instance.cap = cv2.VideoCapture(camera_index)
                    cls._instance.is_demo = False

                # Check if video opened successfully
                if not cls._instance.cap.isOpened():
                    raise ValueError(f"Could not open video source")

            return cls._instance

    @staticmethod
    def _is_webcam_available(index):
        """Check if webcam is available."""
        temp_camera = cv2.VideoCapture(index)
        if temp_camera.isOpened():
            temp_camera.release()
            return True
        return False

    def read(self):
        """Read a frame from the camera or video."""
        success, frame = self.cap.read()

        # For demo mode, loop the video when it ends
        if self.is_demo and not success:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = self.cap.read()

        return success, frame