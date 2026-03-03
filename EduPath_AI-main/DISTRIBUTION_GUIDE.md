# Deployment & Distribution Guide

## 1. How to Run (Testing Phase)
Currently, **Docker** is the *easiest* zero-config way to run the entire backend+database+frontend stack on a developer machine (Windows/Mac/Linux).

To start:
1. install Docker Desktop.
2. Run `docker-compose up` in this folder.
3. Open `http://localhost:5173`.

## 2. How to Run on User Devices (Production)

For end-users (Students/Parents), they will **NOT** use Docker. They will access the app via:

### A. Web Browser (Chromebook, Windows, Mac)
-   **URL**: You will host this app on a cloud server (AWS, Vercel, or DigitalOcean).
-   **Access**: Users simply go to `https://www.edupath.ai` (once you buy the domain).
-   **Installation**: The app is configured as a **PWA (Progressive Web App)**. Chrome will show an "Install EduPath" icon in the address bar, allowing it to look and feel like a native desktop app.

### B. Android & iOS (Mobile App)
To allow installation from the App Store / Play Store without rewriting code:

1.  **Capacitor (Recommended)**:
    -   We can wrap this existing React Web App into a native mobile app container.
    -   Command: `npm install @capacitor/core @capacitor/cli`
    -   Command: `npx cap init`
    -   This generates an `android` and `ios` folder project which you can open in Android Studio / Xcode to build the `.apk` or `.ipa` files.

### C. Offline Usage
-   The PWA configuration (`manifest.json` + Service Workers) allows the app to load even without internet (limited offline mode).

## 3. Deployment Steps (Simplified)

If you don't want to manage servers:
1.  **Frontend**: Deploy the `frontend` folder to **Vercel** or **Netlify** (Free tier). It connects to your GitHub and auto-deploys.
2.  **Backend**: Deploy the `backend` folder to **Render.com** or **Railway.app**.
3.  **Database**: Use a cloud PostgreSQL (e.g., Supabase or Neon.tech).

This setup removes the need for Docker on the user's side completely.
