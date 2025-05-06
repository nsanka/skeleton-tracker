import cv2
from threading import Lock


class Camera:
    """
    Camera class to handle video capture operations.
    Implements a singleton pattern to ensure only one camera instance is used.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, camera_index=0):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Camera, cls).__new__(cls)
                # Initialize the camera
                cls._instance.cap = cv2.VideoCapture(camera_index)
                cls._instance.camera_index = camera_index

                # Check if camera opened successfully
                if not cls._instance.cap.isOpened():
                    raise ValueError(f"Could not open camera with index {camera_index}")
            return cls._instance

    def read(self):
        """
        Read a frame from the camera.

        Returns:
            success: Boolean indicating if read was successful
            frame: The captured frame
        """
        return self.cap.read()

    def release(self):
        """Release the camera resource."""
        self.cap.release()

    def is_opened(self):
        """Check if the camera is opened."""
        return self.cap.isOpened()

    def __del__(self):
        """Destructor to ensure camera resources are released."""
        self.release()