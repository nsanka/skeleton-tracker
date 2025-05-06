FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml README.md ./
COPY skeleton_tracker ./skeleton_tracker
COPY tests ./tests

RUN poetry config virtualenvs.create false \
   && poetry install --no-dev

# Expose the port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Use the client-side app
CMD ["python", "-m", "skeleton_tracker.app_clientside"]
