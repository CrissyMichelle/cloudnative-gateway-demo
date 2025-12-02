# Cloud-Native Gateway Demo

This repo showcases a cloud-native microservices architecture I built as part of my 2025 Cloud Native project work:

- A **FastAPI LLM-style service**
- A **Django login/auth service**
- An **API gateway layer** (KrakenD + Kubernetes Gateway API)
- **Load testing** using Locust

The repo demonstrates how I design and integrate multiple services behind a gateway in a Kubernetes environment, with attention to routing, auth, and performance.

> **Note:** All credentials, private keys, and environment-specific details have been removed or replaced with safe placeholders. This repo is intended purely as a technical portfolio.

---

## Architecture Overview

At a high level, the system looks like this:

**Client (Locust / user) → KrakenD API Gateway → Kubernetes Services → Django Login & FastAPI LLM pods**

- **Django Login Service (`django-login/`)**
  - Provides basic login / user management endpoints.
  - Uses Django + MariaDB (via Kubernetes + Secret manifests).
  - Designed to sit behind the gateway, not be exposed directly to the internet.

- **FastAPI LLM Service (`fastapi-llm/`)**
  - Python FastAPI app exposing an LLM-style `/v1/llm` endpoint.
  - Containerized with Docker and deployed via Kubernetes manifests.
  - Represents a generic AI/ML backend service.

- **API Gateway (`krakend/` + `gateway/`)**
  - **KrakenD** deployment and config for routing, JWT validation, and aggregation.
  - **Gateway API** manifests (HTTPRoutes) to direct traffic from the Kubernetes gateway to Django and FastAPI services.
  - Demonstrates how to front multiple services with a single, consistent API edge.

- **Load Testing (`locusttest/`)**
  - Locust configuration and tests targeting the `/v1/llm` endpoint.
  - Used to generate traffic, observe latency/throughput, and validate behavior under load.

---

## Repository Structure

```text
cloudnative-gateway-demo/
├── django-login/      # Django login/auth service
│   ├── manage.py
│   ├── requirements.txt
│   ├── project/       # Django project (settings.py, urls.py, login app, etc.)
│   ├── docker/        # Dockerfile / build assets for Django
│   └── k8s/           # Kubernetes manifests for the Django service
│
├── fastapi-llm/       # FastAPI LLM-style microservice
│   ├── fastapi_p4/llmserver.py
│   ├── docker/Dockerfile
│   ├── k8s/deployment.yaml
│   ├── k8s/service.yaml
│   ├── poetry.lock / pyproject.toml
│   └── tests/ (if present)
│
├── gateway/           # Kubernetes Gateway API configuration
│   ├── gateway.yaml
│   ├── httproute-django.yaml
│   └── httproute-llm.yaml
│
├── krakend/           # KrakenD API gateway configuration
│   ├── krakend-deployment.yaml
│   ├── krakend-configmap.yaml
│   └── krakend-httproute.yaml
│
├── locusttest/        # Locust load testing project
│   ├── locusttest/locustfile.py
│   ├── pyproject.toml / poetry.lock
│   └── README.md / CSV outputs (optional, may be trimmed for demo)
│
└── .gitignore
