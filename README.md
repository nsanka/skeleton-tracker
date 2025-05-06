# Skeleton Tracker Web

A web application for tracking human skeletons in real-time video using OpenCV, MediaPipe, and Flask.

## Features

- Real-time human pose detection
- Skeleton visualization on original video
- Skeleton-only view on black background
- Web interface for easy access from any device
- FPS calculation and display

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

### Prerequisites

- Python 3.10 or higher
- Poetry
- Webcam or video input device

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/skeleton-tracker-web.git
   cd skeleton-tracker-web
   ```

2. Install dependencies with Poetry
   ```bash
   poetry install
   ```

3. Activate the virtual environment
   ```bash
   poetry shell
   ```

## Usage

### Starting the application

Run the application with Poetry:

```bash
poetry run start
```

Or if you're already in the Poetry shell:

```bash
python -m skeleton_tracker.app
```

### Accessing the web interface

Open your browser and navigate to:

```
http://localhost:5000
```

You should see two video feeds:
- The original webcam feed with skeleton overlay
- A skeleton-only view with black background

### Controls

- **Refresh**: Restarts the video feeds
- **Fullscreen**: Toggles fullscreen view of the video container

## Development

### Project Structure

```
skeleton_tracker_web/
├── pyproject.toml          # Poetry configuration
├── README.md               # This file
├── skeleton_tracker/       # Main package
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Flask application
│   ├── camera.py           # Camera handling
│   ├── tracker.py          # Skeleton tracking logic
│   ├── video_feed.py       # Video feed generation
│   └── templates/          # HTML templates
│       └── index.html      # Web interface
├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_tracker.py     # Tests for tracker module
└── .gitignore              # Git ignore file
```

### Running tests

```bash
poetry run pytest
```

### Code formatting

Format code with Black:

```bash
poetry run black skeleton_tracker tests
```

Sort imports with isort:

```bash
poetry run isort skeleton_tracker tests
```

## License

[MIT](LICENSE)

## Acknowledgements

- [OpenCV](https://opencv.org/) for computer vision capabilities
- [MediaPipe](https://mediapipe.dev/) for pose estimation
- [Flask](https://flask.palletsprojects.com/) for web framework