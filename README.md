# event-management-system
This is my personal project. The point is to create a system where user can manage events and apply RBAC for user access management.

## Getting Started
Follow the instructions below to set up and run your FastAPI project.

### Prerequisites
Ensure you have the following installed:

- Python >= 3.10
- PostgreSQL
- Redis

### Project Setup
1. Clone the project repository:
    ```bash
    git clone https://github.com/Phatcm/event-management-system.git
    ```
   
2. Navigate to the project directory:
    ```bash
    cd event-management-system/
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables by copying the example configuration:

6. Run database migrations to initialize the database schema:
    ```bash
    alembic upgrade head
    ```

## Running the Application
Start the application:

```bash
fastapi dev src/
```