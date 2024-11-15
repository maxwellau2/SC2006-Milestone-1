Here's an enhanced README for your frontend React application:

---

# Frontend Application - Fault Reporting System

This frontend application is a React-based single-page application developed with [Vite](https://vitejs.dev/) for fast development and hot module replacement (HMR). The application integrates with a FastAPI backend and provides a user-friendly interface for reporting, managing, and viewing issue reports.

## Features

-   **User Authentication**: Secure login, registration, and password reset functionality.
-   **Role-Based Access**: Separate access for users, administrators, and authorities, with restricted routes and protected pages.
-   **Report Management**: Users can create and view their own reports, while authorities can manage reports assigned to them.
-   **Admin Panel**: An administration dashboard for managing users and reports, with dedicated pages for management.
-   **Rewards System**: Users can earn rewards for submitting reports, displayed on the `RewardsPage`.
-   **Responsive Design**: Built with a mobile-first approach, optimized for various screen sizes.

## Project Structure

```
frontend/
├── public/               # Static assets
└── src/                  # Source code
    ├── Assets/           # Images, icons, and other static assets
    ├── Common/           # Shared utility functions and components
    └── Components/       # React components for various pages and functionalities
        ├── AdminManagementPage/        # Admin dashboard for managing users and reports
        ├── AdminRestrictedRoute/       # Route protection for admin-only access
        ├── AuthorityMyReport/          # Report management page for authorities
        ├── ForbiddenPage/              # Error page for unauthorized access
        ├── LoginForm/                  # User login form
        ├── MakeReport/                 # Form for submitting new reports
        ├── PasswordResetForm/          # Password reset functionality
        ├── ProfilePage/                # User profile page
        ├── ProtectedRoute/             # Higher-order component for route protection
        ├── RegisterForm/               # User registration form
        ├── RewardsPage/                # Display page for user rewards
        ├── UserDashboard/              # Main dashboard for users
        └── UserMyReport/               # User-specific report viewing page
```

## Technologies

-   **React**: The core framework for building the user interface.
-   **Vite**: For fast development server setup and optimized production builds.
-   **React Router**: For route handling and protected routes.
-   **ESLint**: Code quality and consistency.
-   **SWC**: An alternative to Babel, used for faster builds and HMR.

## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
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

## Available Scripts

-   `npm run dev`: Starts the development server with hot-reload.
-   `npm run build`: Builds the project for production.
-   `npm run preview`: Previews the production build locally.
-   `npm run lint`: Checks code for linting issues.

## Configuration

This project uses a `config.js` file located at the root of the `src` folder to manage configuration values, such as API endpoints. Ensure these values are set correctly for different environments (development, production).

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

---
