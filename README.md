# Camera Check Service

This repository contains a FastAPI based service that analyses camera frames for
common issues such as black screens, occlusions and tampering. Frames are pulled
from Redis streams, processed asynchronously and optional snapshots are stored
in MinIO for later review.

## Features

- Redis backed ingestion of JPEG frames.
- Asynchronous frame analysis using OpenCV and NumPy.
- WebSocket broadcasting of analysis results to connected clients.
- Optional persistence of frames to MinIO with periodic retention policies.

## Requirements

- Python 3.10 or newer.
- Access to a Redis instance for consuming camera frames.
- (Optional) MinIO or an S3 compatible object store if frame persistence is
  required.

Install the Python dependencies with:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Runtime behaviour is controlled via environment variables. Copy
[`.env.example`](.env.example) to `.env` and adjust the values for your
environment:

```bash
cp .env.example .env
```

Key settings include:

- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`: Redis connection
  details used to consume frame data.
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`: Credentials for the
  MinIO/S3 bucket that stores abnormal frames.
- `MINIO_SAVE_MODE`: Controls when frames are persisted (`all`, `abnormal`,
  `sample`, or `none`).
- `ENABLE_TEST_VIDEO`: Enable bundled test video generation utilities for local
  development.

Refer to [`configs/settings.py`](configs/settings.py) and
[`src/main.py`](src/main.py) for the full list of supported options.

## Running the Service

Start the FastAPI application with Uvicorn:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 5020 --reload
```

The API is namespaced under `/pushhub`. Key endpoints:

- `POST /pushhub/start`: Start the background workers.
- `POST /pushhub/stop`: Stop all workers and release resources.
- `POST /pushhub/subscribe`: Provide the list of streams to analyse and optional
  analysis overrides.
- `GET  /docs`: Interactive Swagger UI for exploring the API.
- `WS   /pushhub/ws/results`: Receive analysis results as a WebSocket stream.

## Development Notes

- The default analysis thresholds live in
  [`camera_check_fastapi/src/settings.py`](camera_check_fastapi/src/settings.py)
  and can be overridden through the subscribe endpoint or environment
  variables.
- The worker pool sizes can be tuned through `EXECUTOR_CPU` and `EXECUTOR_IO` in
  [`src/main.py`](src/main.py) to match available hardware.
- Make sure the Redis streams follow the expected schema (`meta` and `jpeg`
  fields) when pushing frames into the system.

## License

This project is provided without a specific license. Add your own licensing
information here if required.
