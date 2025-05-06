import cv2
from skeleton_tracker.camera import Camera
from skeleton_tracker.tracker import SkeletonTracker


class VideoFeed:
    """
    Class to handle video feed generation for Flask routes.
    """
    def __init__(self, camera_index=0):
        """
        Initialize the video feed.

        Args:
            camera_index: Index of the camera to use
        """
        self.camera = Camera(camera_index)
        self.tracker = SkeletonTracker()

    def generate_frames(self):
        """
        Generator function that yields processed video frames.

        Yields:
            bytes: Frame encoded as JPEG in the format expected by Flask's Response
        """
        while self.camera.is_opened():
            success, frame = self.camera.read()
            if not success:
                break

            # Process frame to detect skeletons
            processed_frame = self.tracker.process_frame(frame)

            # Encode the processed frame to JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            # Yield the frame in the required format for a Flask response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def generate_skeleton_frames(self):
        """
        Generator function that yields skeleton-only frames.

        Yields:
            bytes: Skeleton frame encoded as JPEG in the format expected by Flask's Response
        """
        while self.camera.is_opened():
            success, _ = self.camera.read()
            if not success:
                break

            # Get the skeleton-only frame
            skeleton_frame = self.tracker.get_skeleton_frame()

            if skeleton_frame is not None:
                # Encode the skeleton frame to JPEG
                ret, buffer = cv2.imencode('.jpg', skeleton_frame)
                frame_bytes = buffer.tobytes()

                # Yield the frame in the required format for a Flask response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def release(self):
        """Release resources."""
        self.tracker.release()
        self.camera.release()