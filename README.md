# Store Monitor API

The Store Monitor API is a FastAPI-based API that generates reports on store uptime and downtime. It calculates uptime and downtime for the last 1 hour, last 1 day, and last 1 week.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Overview

The Store Monitor API provides a way to calculate and generate reports for store uptime and downtime.

## Features

- Calculates store uptime and downtime.
- Generates reports for the last 1 hour, last 1 day, and last 1 week

## Directory Structure

The project directory is structured as follows:

```
- app
- migrations
- .dockerignore
- .env.example
- .gitignore
- Dockerfile.dev
- Makefile
- README.md
- docker-compose.yml
- pipeline.py
- poetry.lock
- pyproject.toml
- report.csv
- script.py
```

## Installation

1. Clone this repository to your local machine.
2. Create a `.env` file based on `.env.example` and fill in the required configuration.
3. Build and run the Docker container using `docker-compose`:

```bash
docker-compose up --build
```

## Usage

1. Once the container is running, you can access the API documentation at `http://localhost:8000/api/docs`.
2. Use the provided endpoints to calculate and retrieve store uptime and downtime reports.

## Endpoints

- `GET /trigger_report`: Trigger a report generation task
- `POST /get_report`: Get a report for the last 1 hour, last 1 day, or last 1 week for all stores

Refer to the API documentation for detailed information about request and response structures.
