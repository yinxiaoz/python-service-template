# Development

## Prerequisites

- Python 3.13+ via [pyenv](https://github.com/pyenv/pyenv#installation)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)

## Setup

```bash
# Install dependencies
make install
```

## Running Locally

```bash
# Run with Docker
make start-local

# Stop Docker containers
make stop-local
```

## Development Commands

```bash
# Run tests
make test

# Run linter
make lint

# Format code
make format

# Clean cache files
make clean

# Build Docker image
make build
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| HOST | 0.0.0.0 | Server host |
| PORT | 5000 | Server port |
| LOG_LEVEL | INFO | Logging level |
