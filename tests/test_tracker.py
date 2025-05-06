import unittest
import numpy as np
from skeleton_tracker.tracker import SkeletonTracker


class TestSkeletonTracker(unittest.TestCase):
    """Test cases for the SkeletonTracker class."""

    def setUp(self):
        """Set up before each test."""
        self.tracker = SkeletonTracker()

    def tearDown(self):
        """Clean up after each test."""
        self.tracker.release()

    def test_initialization(self):
        """Test that the tracker initializes correctly."""
        self.assertIsNotNone(self.tracker.mp_pose)
        self.assertIsNotNone(self.tracker.mp_drawing)
        self.assertIsNotNone(self.tracker.pose)
        self.assertEqual(self.tracker.prev_time, 0)

    def test_process_empty_frame(self):
        """Test processing an empty frame."""
        # Create a simple black frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = self.tracker.process_frame(frame)

        # Check that the result is the same shape as the input
        self.assertEqual(result.shape, frame.shape)

        # The skeleton frame should be created but will be empty
        self.assertIsNotNone(self.tracker.get_skeleton_frame())

    def test_get_skeleton_frame_before_processing(self):
        """Test getting the skeleton frame before processing any frames."""
        self.assertIsNone(self.tracker.get_skeleton_frame())


if __name__ == '__main__':
    unittest.main()