# Fuel Pass System

A microservices-based system for managing fuel distribution and quotas.

## Project Structure

```text
Fuel Pass/
├── services/
│   ├── citizen-vehicle-service/  - Manages citizens and their vehicles.
│   ├── quota-service/            - Manages fuel quotas and vehicle type quotas.
│   ├── fuel-station-service/     - Manages fuel stations and stock levels.
│   ├── transaction-service/      - Tracks fuel usage and transactions.
│   └── queue-service/            - Manages fuel pump queues.
├── gateway/                     - API Gateway for routing and authentication.
└── README.md
```

## Getting Started

### 1. Prerequisites
- **Python 3.12+**: Ensure Python is installed and added to your PATH.
- **MongoDB**: A running MongoDB instance (local or Atlas).

### 2. Setup Virtual Environment
> [!IMPORTANT]
> All setup and activation commands **MUST** be run from the **project root directory** (`Fuel Pass/`).

1.  **Create the virtual environment**:
    ```powershell
    python -m venv venv
    ```
2.  **Activate the virtual environment**:
    - **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
    - **Windows (CMD)**: `.\venv\Scripts\activate.bat`
3.  **Install all dependencies**:
    ```powershell
    pip install -r services/citizen-vehicle-service/requirements.txt
    pip install -r services/quota-service/requirements.txt
    pip install -r services/fuel-station-service/requirements.txt
    pip install -r services/queue-service/requirements.txt
    pip install -r services/transaction-service/requirements.txt
    pip install -r gateway/requirements.txt
    ```

### 3. Run Services
After activating the virtual environment in your terminal, navigate to the service folder and run it:

| Service | Directory | Command | Port |
| :--- | :--- | :--- | :--- |
| **API Gateway** | `gateway/` | `python main.py` | `8000` |
| **Citizen & Vehicle** | `services/citizen-vehicle-service/` | `python main.py` | `8001` |
| **Fuel Station** | `services/fuel-station-service/` | `python main.py` | `8002` |
| **Queue Service** | `services/queue-service/` | `python main.py` | `8003` |
| **Transaction Service**| `services/transaction-service/` | `python main.py` | `8005` |
| **Quota Service** | `services/quota-service/` | `python main.py` | `8006` |

#### Detailed Steps for Quota Service
1. **Navigate**: Open a new terminal and go to the quota service directory:
   ```powershell
   cd services/quota-service
   ```
2. **Setup**: (Optional) Ensure dependencies are installed:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run**: Start the service using Python:
   ```powershell
   python main.py
   ```
4. **Verify**: Access the API documentation at `http://localhost:8006/api-docs`.

> [!TIP]
> Each service has its own Swagger documentation at `http://localhost:<PORT>/api-docs`. The unified documentation is available at `http://localhost:8000/api-docs`.

## Troubleshooting

### "Fatal error in launcher" or "No Python at..."
If you see errors like `Fatal error in launcher` or `No Python at 'C:\Python312\python.exe'`, your virtual environment is broken (likely due to path changes).

**Fix**: Delete the `venv` folder and recreate it:
1. Delete: `Remove-Item -Recurse -Force venv` (PowerShell) or `rd /s /q venv` (CMD)
2. Re-run the **Setup Virtual Environment** steps above.

### "Term is not recognized"
If you get an error saying `.\venv\Scripts\activate` is not recognized, ensure you are in the **project root** directory (where the `venv` folder is located), not inside a `services/` sub-folder.
