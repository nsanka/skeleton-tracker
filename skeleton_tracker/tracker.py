import cv2
import mediapipe as mp
import numpy as np
import time


class SkeletonTracker:
    """
    A class for tracking human skeletons in video frames using MediaPipe.
    """

    def __init__(self):
        """Initialize the skeleton tracker with MediaPipe pose detection."""
        # Initialize MediaPipe Pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        # Drawing specs for better visualization
        self.drawing_spec = self.mp_drawing.DrawingSpec(
            color=(0, 255, 0),
            thickness=2,
            circle_radius=2)

        # For FPS calculation
        self.prev_time = 0
        self.current_time = 0

        # Store the most recent skeleton-only frame
        self.skeleton_frame = None

    def process_frame(self, frame):
        """
        Process a single frame to detect and draw human skeletons.

        Args:
            frame: The input video frame in BGR format

        Returns:
            annotated_frame: The original frame with skeleton overlay
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for pose detection
        results = self.pose.process(rgb_frame)

        # Draw skeleton on the frame
        annotated_frame = frame.copy()

        # Create a black canvas for skeleton-only view
        h, w, c = frame.shape
        black_canvas = np.zeros((h, w, c), dtype=np.uint8)

        if results.pose_landmarks:
            # Draw the pose landmarks on the original frame
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)

            # Draw skeleton on black background for clearer visualization
            self.mp_drawing.draw_landmarks(
                black_canvas,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)

        # Store the skeleton frame
        self.skeleton_frame = black_canvas

        # Calculate and display FPS
        self.current_time = time.time()
        fps = 1 / (self.current_time - self.prev_time) if self.prev_time > 0 else 0
        self.prev_time = self.current_time

        # Display FPS on the frame
        cv2.putText(annotated_frame, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return annotated_frame

    def get_skeleton_frame(self):
        """Return the most recent skeleton-only frame."""
        return self.skeleton_frame

    def release(self):
        """Release resources."""
        self.pose.close()