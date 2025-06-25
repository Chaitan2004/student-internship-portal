# **Internship Monitoring Software for ECIL.co**

This project is designed to provide a robust solution for monitoring and managing student internships, tailored specifically for ECIL.co. It leverages modern software development techniques to ensure seamless tracking, reporting, and oversight of internships in real-time.

## Prerequisites

Before you start, make sure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) — for containerizing and running the app
- [Docker Compose](https://docs.docker.com/compose/install/) — usually included with Docker Desktop, used to manage multi-container Docker applications
- [Git](https://git-scm.com/downloads) — to clone the project repository

---

## Step 1: Clone the Repository

Open your terminal (Linux/macOS) or Command Prompt/PowerShell (Windows) and run:

```bash
git clone https://github.com/Chaitan2004/student-internship-portal.git
cd student-internship-portal
```
## Step 2: Build the application

Double-click on the `build.bat` file located in the project folder.  
This will build the Docker images needed for the application.

## Step 3: Start the application

After building, double-click on the `start.bat` file.  
This will start the application containers and open the app in your default browser automatically.

### Steps for linux
Run these commands:
```bash
docker-compose build && echo "✅ Build complete!"
docker-compose up -d
sleep 5
xdg-open http://localhost:5000
```
