# CS212 Web Application Boilerplate

This repository contains the reference implementation for the full-stack web application assignment. It demonstrates the integration of a Vue.js frontend with a FastAPI backend, utilizing Docker for containerization and Vercel for serverless deployment.

## System Architecture

The application is composed of two primary services:

*   **Frontend**: A Single Page Application (SPA) built with Vue 3 and Vite. It serves the user interface and communicates with the backend via RESTful API calls.
*   **Backend**: A Python-based REST API built with FastAPI. It handles data persistence, business logic, and authentication (JWT + Google OAuth).
*   **Database**: PostgreSQL is used for relational data storage. The application is configured to switch between a local Dockerized instance and a remote Supabase instance based on environment configuration.

## Project Structure

```
├── fastapi/          # Backend application source code
│   ├── app/          # Core application logic (routers, models, schemas)
│   ├── main.py       # Application entry point
│   └── requirements.txt
├── frontend/         # Frontend application source code
├── docker-compose.yml # Container orchestration configuration
├── vercel.json       # Deployment configuration for Vercel
├── run.sh            # Utility script for local environment initialization
└── .env.example      # Environment variable template
```

## Local Development Setup

The project is designed to run in a containerized environment using Docker.

### 1. Environment Configuration

Copy the example configuration file and update the values with your credentials.

```bash
cp .env.example .env
```

### 2. Service Initialization

Execute the initialization script to start the services. This script automatically detects the database configuration.

```bash
./run.sh
```

**Database Modes:**
*   **Local**: Uses a local PostgreSQL container (Default).
*   **Remote**: Set `USE_SUPABASE=true` in `.env` to connect to a managed Supabase instance.

### 3. Access Points

*   **Frontend**: `http://localhost:8080`
*   **API Documentation**: `http://localhost:56733/docs` (Direct) or `http://localhost:8080/api/docs` (Proxied)

## Deployment (Vercel)

The application is configured for deployment on the Vercel platform.

1.  **Installation**: Ensure the Vercel CLI is installed.
    ```bash
    npm i -g vercel
    ```

2.  **Deployment**:
    ```bash
    vercel --prod
    ```

### Configuration Requirements

Verify the following settings in the Vercel Project Dashboard:

*   **Environment Variables**:
    *   `SUPABASE_DB_URL`: Connection string for the production database.
    *   `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: OAuth credentials.
    *   `SECRET_KEY` / `JWT_SECRET_KEY`: Cryptographic signing keys.
    *   `APP_ENV`: Set to `production`.

*   **Build Settings**: Default settings are overridden by `vercel.json` and do not require manual configuration.

## Authentication

Authentication is implemented using JSON Web Tokens (JWT) and OAuth 2.0.

*   **Google OAuth**: Requires valid credentials from the Google Cloud Console.
    *   **Local Redirect URI**: `http://localhost:56733/google/auth`
    *   **Production Redirect URI**: `https://<your-project>.vercel.app/api/google/auth`

## Dependency Management

Dependencies are managed separately for each service:

*   **Frontend**: `npm install` (within `frontend/` directory)
*   **Backend**: `pip install -r requirements.txt` (within `fastapi/` directory)