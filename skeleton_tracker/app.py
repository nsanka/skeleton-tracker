import atexit
import os
from flask import Flask, render_template, Response
from skeleton_tracker.video_feed import VideoFeed

# Create Flask application
app = Flask(__name__)

# Create a video feed instance
video_feed = VideoFeed()

@app.route('/')
def index():
    """
    Render the homepage with video streams.

    Returns:
        rendered HTML template
    """
    return render_template('index.html')

@app.route('/video_feed')
def video_feed_route():
    """
    Route for the main video feed.

    Returns:
        Flask Response with video stream
    """
    return Response(video_feed.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/skeleton_feed')
def skeleton_feed_route():
    """
    Route for the skeleton-only video feed.

    Returns:
        Flask Response with skeleton stream
    """
    return Response(video_feed.generate_skeleton_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def cleanup():
    """Clean up resources when the application exits."""
    video_feed.release()

# Register cleanup function to run when application exits
atexit.register(cleanup)


def main():
    """Main function to run the Flask application."""
    try:
        # Use environment port if available (for cloud deployment)
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup()

if __name__ == '__main__':
    main()