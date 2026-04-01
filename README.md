# Fuel Pass System

A microservices-based system for managing fuel distribution and quotas.

## Project Structure

```text
Fuel Pass/
├── services/
│   ├── citizen-vehicle-service/  - Manages citizens, their vehicles, and fuel quotas.
│   ├── station-service/          - (Planned) Manages fuel stations and stock levels.
│   ├── transaction-service/      - (Planned) Tracks fuel usage and transactions.
│   └── queue-service/            - (Planned) Manages fuel pump queues.
├── gateway/                     - (Planned) API Gateway for routing and authentication.
└── README.md
```

## Getting Started

### Citizen & Vehicle Service
1. Navigate to the service directory:
   ```bash
   cd services/citizen-vehicle-service
   ```
2. Install dependencies (using the root virtual environment):
   ```bash
   ../../venv/Scripts/pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   ../../venv/Scripts/python main.py
   ```

### API Gateway
1. Navigate to the gateway directory:
   ```bash
   cd gateway
   ```
2. Install dependencies:
   ```bash
   ../venv/Scripts/pip install -r requirements.txt
   ```
3. Run the gateway:
   ```bash
   ../venv/Scripts/python main.py
   ```
4. Access the unified API documentation:
   - URL: `http://localhost:8000/api-docs`
