# Guide to the SC2006 Project Backend

## Setup on WINDOWS WSL

0. Retrieve config.py from the anyone else who has it

```
just ask maxwell first, he'll give it to you
```

1. Install Python 3.11

```
sudo apt update && upgrade
sudo apt install python3 python3-pip
```

2. clone the repo

```
git clone git@github.com:maxwellau2/ReportQuestBackend.git
cd ReportQuestBackend
```

3. Instantiate the virtual environment

```
python3 -m venv venv
```

4. Activate the virtual environment

```
source venv/bin/activate
```

5. Install dependencies as stated in requirements.txt

```
pip install -r "requirements.txt"
```

6. Run the migrations to create the databases

```
make migrate-up
```

7. Installing ollama

```
curl -fsSL https://ollama.com/install.sh | sh

ollama pull llama3.2

ollama pull llava

# to test:

ollama run ollama3.2
```

8. Run the main.py, ensure you are in root directory

```
# activate the GPU if applicable
make enable-ollama-gpu
# run the main.py
make run-reloadable
```

9. To test the application, open http://0.0.0.0:8000/docs in your browser and test endpoints

---

### **File Structure Overview**

This project is organized as follows:

-   **Root Directory**:
    -   **`CHECKPOINT.md`**: Checkpoint documentation or notes related to project progress.
    -   **`README.md`**: Main documentation file describing the project, installation, and usage instructions.
    -   **`Makefile`**: Contains commands to automate common tasks in the project.
    -   **`config.py`**: Configuration settings for the application.
    -   **`requirements.txt`**: Lists Python dependencies.
    -   **`main.py`**: Main entry point of the application.
    -   **`migrate.py`**: Handles database migrations.
    -   **`seed.py`**: Seeds initial data into the database.
-   **`database/`**:

    -   Contains various SQLite databases used by the application (`authorities.csv`, `authority.db`, `myRewards.db`, `points.db`, `posts.db`, `reports.db`, `rewards.db`, `users.db`).

-   **`database_seeder/`**:

    -   Scripts to populate specific tables in the database:
        -   **`seedAuthority.py`**: Seeds data for authority information.
        -   **`seedMyRewards.py`**, **`seedReports.py`**, **`seedRewards.py`**, and **`seedUsers.py`**: Populate data for their respective tables.

-   **`img/`**:

    -   Contains image assets organized by type:
        -   **`postImages/`**, **`profilepics/`**, **`reportimg/`**, and **`voucherimg/`** directories, each containing specific images.

-   **`src/`**:
    -   **`login/`**: Contains modules and logic related to user login.
    -   **`middleware/verifyJWT.py`**: Middleware to verify JSON Web Tokens for user authentication.
    -   **`migrations/`**: Scripts for creating and managing database tables and structures (e.g., `createUserTable.py`, `createReportsTable.py`, etc.).
    -   **`posts/`**:
        -   **`controllers/ControllerPosts.py`**: Manages post-related API endpoints.
        -   **`models/`**: Contains data models for posts (`AuthorityModel.py`, `PostModel.py`).
        -   **`services/`**: Business logic for posts (`AuthorityService.py`, `PostService.py`).
        -   **`test_api/`** and **`test_unit/`**: Test files for post services and controllers.
    -   **`reports/`**:
        -   **`controllers/ControllerReports.py`**: Manages report-related API endpoints.
        -   **`models/`**: Data models for reports (`PointsModel.py`, `ReportModels.py`).
        -   **`services/`**: Business logic for handling reports (`OllamaAsync.py`, `PointsService.py`, `ReportService.py`, `telegramBot.py`).
        -   **`test_api/`** and **`test_unit/`**: Test files for report services and controllers.
    -   **`rewards/`**:
        -   **`controllers/ControllerReward.py`**: Manages reward-related API endpoints.
        -   **`models/`**: Data models for rewards (`MyRewards.py`, `RewardModel.py`).
        -   **`services/RewardService.py`**: Contains business logic for rewards.
        -   **`test_api/`** and **`test_unit/`**: Test files for reward services and controllers.
    -   **`users/`**:
        -   **`controllers/`**: Manages user-related API endpoints (`ControllerPublic.py`, `ControllerUser.py`).
        -   **`models/`**: User-related models (`PasswordReset.py`, `UnverifiedUsers.py`, `UserModels.py`).
        -   **`services/`**: Business logic for handling users (`AuthService.py`, `UserService.py`).
        -   **`test_api/`** and **`test_unit/`**: Test files for user services and controllers.

Each directory contains logically grouped files and follows a modular structure, making the project more maintainable and organized.
