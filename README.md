# fastapi-ci-docker-pipeline

# FastAPI CI Pipeline with Docker Compose

This project demonstrates a container-based CI testing pipeline for a FastAPI application using Docker Compose.

The API under test is provided as a pre-built Docker image:
datascientest/fastapi:1.0.0

Each test suite runs in an isolated container, simulating independent CI jobs in a real DevOps pipeline.

---

## Architecture

The pipeline is composed of 4 services:

- api  
  FastAPI application container

- test_auth  
  Validates authentication using the /permissions endpoint

- test_authorization  
  Validates user access rights to model versions

- test_content  
  Validates sentiment score polarity on sample inputs

All services communicate through a Docker network and share a volume to aggregate logs.

Execution order:
api → test_auth → test_authorization → test_content

---

## API Endpoints Tested

- GET /status  
  Health check

- GET /permissions  
  Authentication validation

- GET /v1/sentiment  
  Old sentiment model

- GET /v2/sentiment  
  New sentiment model

---

## Tests Description

### Authentication Tests

Endpoint:
- /permissions

Test cases:
- alice / wonderland → 200
- bob / builder → 200
- invalid credentials → 403

---

### Authorization Tests

Endpoints:
- /v1/sentiment
- /v2/sentiment

Rules:
- bob → access to v1 only
- alice → access to v1 and v2

---

### Content Validation Tests

User:
- alice

Sentences tested:
- "life is beautiful" → positive score
- "that sucks" → negative score

Validated on:
- v1 model
- v2 model

The test verifies the sign of the returned sentiment score.

---

## How to Run the Pipeline

Requirements:
- Docker
- Docker Compose

Run all tests:

```bash
chmod +x setup.sh
./setup.sh