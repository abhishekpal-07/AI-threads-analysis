# 🛡️ AI-Powered Cloud-Native Log Analytics & Threat Detection Platform

An enterprise-grade, high-scale Microservices application designed to stream server logs, analyze anomalies/cyber threats in real-time using an AI heuristics engine, and persist reports securely. Fully containerized and automated with a DevOps CI/CD workflow.

---

## 🏗️ Architecture & Flow Overview

The platform consists of 5 core decoupled services communicating over an isolated Docker bridge network:

1. **Log Generator (Node.js/Express):** Continuously simulates distributed server events (INFO, WARNING, CRITICAL logs) and injection attack patterns.
2. **Message Broker (Redis Queue):** Acts as a high-throughput FIFO queue (`LPUSH/RPOP`) buffer to handle peak traffic spikes and prevent data loss.
3. **AI Threat Engine (Python FastAPI):** An asynchronous backend processor that filters incoming logs, calculates threat confidence scores, and detects critical security risks.
4. **Data Store (MongoDB):** A permanent, container-isolated transactional database storing threat signatures and system alert history.
5. **Dashboard UI (Nginx):** A production-grade frontend monitoring system that displays live health states and server telemetry.

---

## 🛠️ Tech Stack & DevOps Practices

- **Languages:** Node.js, Python 3.9, HTML5/JavaScript
- **Frameworks:** Express.js, FastAPI
- **Databases & Queues:** MongoDB, Redis 7 (Alpine)
- **Containerization & Orchestration:** Docker, Docker Compose (Multi-Stage Builds, Non-Root Users, Architectural Platform Restrictions)
- **CI/CD Automation:** Parallel Build GitHub Actions Workflows
- **Web Server:** Nginx (Alpine)

---

## 🚀 Key DevOps & Performance Features Implemented

*   **Docker Multi-Stage Optimization:** Reduced Python/Node image footprint by up to 70% using build layers isolation and lightweight Alpine base runtimes.
- **Production Hardening (Non-Root Privileges):** Configured application contexts under strict non-root user permissions (`USER node`) to secure execution against container escape attacks.
*   **Asynchronous Processing:** Built non-blocking background workers utilizing Python `asyncio` loop queues to prevent runtime thread freezing during peak load analytics.
*   **Resilient Network Connectivity:** Coded exponential retry connectivity structures inside application pipelines to cleanly tolerate network database initialization delays.
*   **Isolated Custom Bridge Networking:** Separated microservices architecture cleanly through decoupled logical network namespaces inside Compose topologies.

---

## ⚙️ How to Spin Up the Platform Locally

### Prerequisites:
Make sure you have **Docker Desktop** installed and running on your machine.

### Execution Steps:
1. Clone this repository:
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd ai-devops-log-platform
   ```

2. Provision and build the entire environment infrastructure in one shot:
   ```bash
   docker compose up --build -d
   ```

3. Verify infrastructure run state:
   ```bash
   docker compose ps
   ```

4. Launch the Operational Monitoring Dashboard:
   Open your browser and navigate to **`http://localhost:8080`**