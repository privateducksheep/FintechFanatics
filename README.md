# XRPL Hackathon Project

This repository contains the full-stack setup for our XRPL hackathon project.

---

## 🧱 Project Structure

root/
├── services/
│ ├── api/ # FastAPI backend (localhost:8000)
│ └── xrpl/ # XRPL Node service (localhost:3001)
│
├── apps/
│ └── mobile/ # Expo mobile app
│
├── .env.example
└── README.md

yaml
Copy code

---

## 🛠 Prerequisites

Install these before starting:

- Node.js **v18+**
- Python **3.10+**
- npm
- Expo Go (mobile app)
- Git

---

## 🚀 How to Run the Project

⚠️ You need **3 terminals open at the same time**

---

### 1️⃣ XRPL Service (Port 3001)

```bash
cd services/xrpl
npm install
node index.js
✅ You should see:

nginx
Copy code
XRPL service listening on http://localhost:3001
2️⃣ Backend API (Port 8000)
bash
Copy code
cd services/api
python -m venv venv
source venv/bin/activate     # macOS / Linux
pip install fastapi uvicorn python-dotenv
pip install httpx
python -m uvicorn main:app --reload --port 8000
✅ You should see:

nginx
Copy code
Uvicorn running on http://127.0.0.1:8000
3️⃣ Mobile App (Expo)
bash
Copy code
cd apps/mobile
npm install
npx expo start
Scan QR code using Expo Go

Or run on emulator

🔌 Ports Summary
Service	URL
XRPL Service	http://localhost:3001
Backend API	http://localhost:8000
Expo Dev Server	http://localhost:19000

✅ How to Verify Everything Is Running
XRPL Service
Terminal shows:

nginx
Copy code
XRPL service listening on http://localhost:3001
Open browser: http://localhost:3001

Backend API
Terminal shows:

nginx
Copy code
Uvicorn running on http://127.0.0.1:8000
Open browser: http://localhost:8000
(You should see JSON or FastAPI docs)

Mobile App
Expo Dev Tools opens in browser

App loads without a red error screen

📱 IMPORTANT: Using a Physical Phone
If you are running the mobile app on a real phone, you CANNOT use localhost.

Replace localhost with your laptop’s LAN IP.

Example:

cpp
Copy code
http://192.168.1.5:8000
Find your IP (macOS):
bash
Copy code
ipconfig getifaddr en0
🧑‍🤝‍🧑 Git Workflow
main → stable

dev → active development

Feature branches → feature/<name>

❗ Common Issues
Port already in use → stop old process

Mobile cannot reach backend → use laptop IP, not localhost

Expo stuck → run:

bash
Copy code
npx expo start -c

📌 Notes
Everyone runs services locally

Do NOT commit .env or venv

Use .env.example to create your own .env

yaml
Copy code

---

## ✅ What to do now
1. Replace README with the above
2. Save
3. Run:
```bash
git add README.md
git commit -m "Fix README to match actual server setup"
git push