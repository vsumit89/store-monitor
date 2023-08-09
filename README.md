# Store Monitor API

The Store Monitor API is a FastAPI-based API that generates reports on store uptime and downtime. It calculates uptime and downtime for the last 1 hour, last 1 day, and last 1 week.

## Architecture Diagram

![Architecture Diagram](./images/store-monitor.drawio.svg)

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

**app**: This is where the main application code resides. It's divided into subdirectories based on functionality for better organization.

**app/db**: Contains database-related code and configurations.

**app/models**: Defines data models and database schema.
routes: Houses API route definitions.

**app/schema**: Contains Pydantic schema definitions for request and response validation.

**app/service**: Holds the business logic and service layer implementations.

**app/utils**: Contains utility modules and helper functions used throughout the application.

**app/main.py**: The entry point of the FastAPI application.

**images**: Store system architecture diagrams and other relevant images here.

**migrations**: Contains initial SQL files used for setting up the initial database tables.

**.env.example**: An example file that lists the environment variables needed for the application. Developers can copy this file and customize it for their local environment.

**docker-compose.yml**: Defines the configuration for Docker Compose to set up various services required for the application.

**Dockerfile.dev**: Dockerfile for creating a development environment container.

**Makefile**: Contains useful commands for development tasks, making common tasks easily executable.

**pipeline.py**: Script to load data from CSV files into DataFrames.

## Steps to run the project

1. Clone this repository to your local machine.
2. Create a `.env` file based on `.env.example` and fill in the required configuration.
3. Build and run the Docker container using `docker-compose`:

```bash
docker-compose up --build
```

## Steps to ingest data

1. Create a `datastore` folder in the root directory of the project.
2. Inside that create
   - store_business_hours.csv
   - store_status.csv
   - store_timezone.csv
3. Once the container is running, run the following command to ingest data into the database

```bash
docker exec -it store-monitor-api python pipeline.py
```

## Usage

1. Once the container is running, you can access the API documentation at `http://localhost:8000/api/docs`.
2. Use the provided endpoints to calculate and retrieve store uptime and downtime reports.

## Endpoints

- `GET /trigger_report`: Trigger a report generation task
- `POST /get_report`: Get a report for the last 1 hour, last 1 day, or last 1 week for all stores

Refer to the API documentation for detailed information about request and response structures.
