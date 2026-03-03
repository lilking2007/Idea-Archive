# EduPath AI 🎓
> *Personalized Curriculum Learning Platform & AI Study Assistant*

**EduPath AI** is a cross-platform educational application designed to empower parents and children. It auto-generates curriculum-aligned learning roadmaps, tracks progress in real-time, and provides a safe, gamified environment for students.

![Project Status](https://img.shields.io/badge/Status-MVP%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🌟 What This Application Does

### For Students:
- **Visual Roadmaps**: See a clear path of what to learn next (e.g., "Algebra Basics" -> "Linear Equations").
- **Interactive Content**: Watch videos, read articles, and take quizzes directly in the app.
- **Gamification**: Earn badges and streaks to stay motivated.
- **Focus Mode**: Distraction-free interface designed for learning.

### For Parents:
- **Dashboard**: View real-time stats (Time spent, Topics mastered).
- **Control**: toggle study modes and view detailed progress reports.
- **Peace of Mind**: Safe, curated content aligned with school standards.

---

## 🛠️ Installation & Setup (For Developers)

This repository contains the full source code. You can run it locally to test or modify it.

### Prerequisites in order to run locally
- **Docker Desktop** (Recommended for easiest setup)
- *OR* **Node.js** (v18+) and **PostgreSQL** installed manually.

### Option 1: Run with Docker (Recommended)
This method installs the database, backend, and frontend automatically.

1.  **Clone this repository** (or download the files).
2.  Open a terminal in the project folder.
3.  Run:
    ```bash
    docker-compose up --build
    ```
4.  Wait for the logs to say "Nest application successfully started".
5.  Open your browser:
    -   **Web App**: [http://localhost:5173](http://localhost:5173)
    -   **API Server**: [http://localhost:3000](http://localhost:3000)

### Option 2: Run Manually (No Docker)
1.  **Backend**:
    ```bash
    cd backend
    npm install
    npm run start:dev
    ```
2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

---

## 🚀 How to "Install" on Devices (End Users)

EduPath AI is built as a **Progressive Web App (PWA)**. This means it works on all devices without needing a heavy download.

### Windows, Mac, & Chromebook
1.  **Host the Website**: You (the developer) must deploy this code to a web host (see "Deploying" below).
2.  **Visit the URL**: Users go to your website (e.g., `www.edupath.ai`).
3.  **Install**: They click the "Install" icon in the browser address bar.
    -   *Result*: The app installs to their desktop, gets an icon, and runs in its own window like a native app.

### Android & iOS
1.  **Web Access**: Can be installed via browser ("Add to Home Screen").
2.  **App Store**: To be listed in the App Store, you must wrap this code using **Capacitor**:
    -   Run `npx cap init` in the frontend folder.
    -   Build the native project (Requires Android Studio / Xcode).

---

## 🌐 Deploying from GitHub

### Can I launch this directly from GitHub?
**Partially.**

1.  **The Frontend (User Interface)**:
    -   ✅ YES. You can host the `frontend` on **GitHub Pages**, **Vercel**, or **Netlify**.
    -   This will make the website publicly accessible.

2.  **The Backend (Logic & Database)**:
    -   ❌ NO. GitHub does not host running servers or databases.
    -   You must deploy the `backend` folder to a service like **Render**, **Railway**, or **Heroku**.

### Recommended Deployment Stack (Free Tiers available)
1.  **Frontend**: Vercel (Connects to your GitHub repo -> Auto-deploys).
2.  **Backend**: Render.com (Hosts the Node.js API).
3.  **Database**: Neon.tech (Free Serverless PostgreSQL).

Once these are linked, you will have a live URL (e.g., `https://edupath-app.vercel.app`) that you can share with anyone on Windows, Mac, or Chromebook.

---

## 📂 Repository Structure

-   `/backend`: **NestJS API**
    -   Handles user logic, database connections, and roadmap generation.
-   `/frontend`: **React + Vite App**
    -   The visual interface for Parents and Students.
-   `docker-compose.yml`: Configuration to run everything together.

---

## � Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---
**EduPath AI** - Built for the future of education.
