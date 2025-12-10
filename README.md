# DevOps Live Services Dashboard

A real-time monitoring and control dashboard for DevOps services using Docker, PostgreSQL, Redis, and RabbitMQ.

This application allows users to monitor, start, stop, and ping essential services in real-time, with persistent logs stored in PostgreSQL. It is designed to showcase live infrastructure status and functionality, ideal for demonstrations, DevOps learning, or internal monitoring.

Table of Contents

1. Features

2. Architecture

3. Prerequisites

4. Installation

5. Usage

6. File Structure

7. Technologies Used


Features

* Real-time status monitoring of PostgreSQL, Redis, and RabbitMQ.

* Start/Stop services via the web interface.

* Ping functionality to check live connectivity for each service.

* Persistent logs stored in PostgreSQL.

* Live event display for each service, updated dynamically.

## Architecture

The application consists of:

### Frontend:

* HTML, CSS, and JavaScript:

  - Displays service status, logs, and control buttons.

  - Fetches logs and status from backend API.

### Backend:

* FastAPI application running in Docker:

  - Manages service control (start/stop), pings, and logs.

  - Stores logs in PostgreSQL for persistence and sharing.

### Services:

* PostgreSQL: Stores logs and supports DB connectivity tests.

* Redis: In-memory cache service.

* RabbitMQ: Message queue service.

All services run in Docker containers using a shared network.

## Prerequisites

* Docker and Docker Compose installed.

* Basic understanding of DevOps services: PostgreSQL, Redis, RabbitMQ.

## Installation

Clone the repository:

```bash 
git clone https://github.com/yourusername/devops-live-dashboard.git
cd devops-live-dashboard
```

Build and start all services using Docker Compose:

``` bash 
docker compose up --build
```

This will start:

- Backend FastAPI server (localhost:8000).

- Frontend dashboard (localhost:8080).

- PostgreSQL, Redis, and RabbitMQ services.

## Usage

Open the dashboard in your browser:

``` bash
http://localhost:8080
```

### Monitor services:

Each service panel displays "Online" or "Offline" status.

Status updates automatically every 2 seconds.

### Control services:

Click Stop to stop a service.

Click Start to start a service.

Click Ping to check connectivity (logs recorded in PostgreSQL)

### View logs:

Each service panel has an events window showing historical and real-time logs.

Logs are persistent and survive page reloads, unless you stop the Postgres service (logs will not be written into the DB).

## File Structure:

``` bash 
devops-live-dashboard/
├─ backend/
│  ├─ app.py            
│  ├─ requirments.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ index.html        
│  ├─ style.css         
│  └─ script.js         
├─ docker-compose.yaml  
└─ README.md           
```
---

## Technologies Used

- Frontend: HTML, CSS, JavaScript

- Backend: Python, FastAPI

- Database: PostgreSQL (persistent logs)

- Services: Redis, RabbitMQ

- Containerization: Docker & Docker Compose

---

## License

This project is open-source and available under the MIT License.

---

### Created with ❤️ for DevOps monitoring and learning purposes