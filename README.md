# ReportQuest Project

This project is a fault reporting system built with a **React frontend** and a **FastAPI backend**. Users can report issues, view reports, and earn rewards, while administrators and authorities can manage reports and user data.

## Table of Contents

-   [Project Overview](#project-overview)
-   [Technologies](#technologies)
-   [Setup](#setup)
    -   [Docker Setup](#docker-setup)
    -   [Frontend Setup](#frontend-setup)
    -   [Backend Setup](#backend-setup)
-   [File Structure Overview](#file-structure-overview)
-   [Usage](#usage)
-   [Contributing](#contributing)
-   [License](#license)

---

## Project Overview

The ReportQuest project provides a platform for users to submit issue reports with multimedia support, receive rewards, and allows admins and authorities to manage these reports effectively. The project consists of:

-   **Frontend**: A React single-page application built with Vite, offering a responsive and user-friendly interface.
-   **Backend**: A FastAPI server that handles user authentication, report management, and business logic for rewards and points, utilizing SQLite databases.

## Technologies

-   **Frontend**:
    -   React, Vite, React Router
    -   ESLint, SWC (alternative to Babel for fast builds)
-   **Backend**:
    -   FastAPI, SQLite
    -   JWT authentication, Ollama for AI-based report evaluations
    -   Docker compatibility for streamlined deployment

---

## Setup

### Prerequisites

-   **Python 3.11** or later
-   **Node.js** and **npm**
-   **Docker** and **Docker Compose** for containerized setup
-   **WSL** (Windows Subsystem for Linux) for Windows users

### Docker Setup

You can run both the frontend and backend with Docker Compose for an easy, containerized setup.

1. **Clone the repository**:

    ```bash
    git clone git@github.com:maxwellau2/SC2006-Milestone-1.git
    cd ReportQuest
    ```

2. **Build and run with Docker Compose**:

    ```bash
    docker-compose up --build
    ```

    This command will build and start the backend and frontend services, along with an SQLite database service.

3. **Access the application**:

    - **Frontend**: [http://localhost:5173](http://localhost:5173)
    - **Backend API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend Setup (Without Docker)

1. **Navigate to the frontend directory**:

    ```bash
    cd frontend
    ```

2. **Install dependencies**:

    ```bash
    npm install
    ```

3. **Run the application**:

    ```bash
    npm run dev
    ```

4. **Build for production**:

    ```bash
    npm run build
    ```

5. **Preview the production build**:

    ```bash
    npm run preview
    ```

### Backend Setup (on Windows WSL or Without Docker)

1. **Retrieve `config.py`**:

    Reach out to Maxwell for a copy of `config.py` with necessary configuration settings.

2. **Install Python 3.11**:

    ```bash
    sudo apt update && sudo apt upgrade
    sudo apt install python3 python3-pip
    ```

3. **Navigate to the backend directory**:

    ```bash
    cd backend
    ```

4. **Set up the virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

5. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

6. **Run database migrations**:

    ```bash
    make migrate-up
    ```

7. **Install Ollama (for AI functionality)**:

    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull llama3.2
    ollama pull llava
    ```

8. **Run the application**:

    ```bash
    make enable-ollama-gpu  # (optional, if GPU is available)
    make run-reloadable
    ```

9. **Access the API documentation**:

    Open [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) to explore API endpoints.

---

## File Structure Overview

### Frontend

```
frontend/
├── public/                    # Static assets
└── src/                       # Source code
    ├── Assets/                # Static images and icons
    ├── Common/                # Shared utilities and components
    └── Components/            # Main UI components and pages
```

### Backend

```
backend/
├── main.py                    # Application entry point
├── config.py                  # Configuration settings (external, private)
├── requirements.txt           # Python dependencies
├── database/                  # SQLite databases
├── database_seeder/           # Scripts for seeding initial data
├── src/
│   ├── login/                 # Login and JWT authentication logic
│   ├── middleware/            # JWT verification
│   ├── posts/                 # Post management modules
│   ├── reports/               # Report management modules
│   ├── rewards/               # Rewards logic and controllers
│   └── users/                 # User-related endpoints and services
```

---

## Usage

-   **Frontend**: Run `npm run dev` in the frontend directory to start the development server.
-   **Backend**: Run `make run-reloadable` in the backend directory to start the FastAPI server.
-   **Docker Compose**: Run `docker-compose up --build` in the root directory to start the entire application in Docker.

Once both are running, you can test the application by accessing the frontend interface and backend API documentation at their respective URLs.

---

## Contributing

1. **Fork the repository**.
2. **Create a feature branch**: `git checkout -b feature/YourFeature`.
3. **Commit your changes**: `git commit -m 'Add some feature'`.
4. **Push to the branch**: `git push origin feature/YourFeature`.
5. **Open a pull request**.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

This README provides a comprehensive overview of the project, setup instructions (including Docker setup), and usage details for both the frontend and backend. Let me know if you'd like further adjustments!
