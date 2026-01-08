# XRPL Hackathon Project

This repo contains the full-stack setup for our XRPL hackathon project.

---

## 🧱 Project Structure

root/
├── backend/        # Django / API (localhost:8000)
├── xrpl-service/   # XRPL service (localhost:3001)
├── mobile/         # Expo mobile app
└── README.md

---

## 🛠 Prerequisites

- Node.js (v18+)
- Python 3.10+
- npm or yarn
- Expo Go app
- Git

---

## 🚀 How to Run the Project

⚠️ You need **3 terminals running at the same time**

---

### 1️⃣ XRPL Service (Port 3001)

cd xrpl-service  
npm install  
npm run dev  

---

### 2️⃣ Backend API (Port 8000)

cd backend  
python -m venv venv  
source venv/bin/activate   # macOS  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  

---

### 3️⃣ Mobile App (Expo)

cd mobile  
npm install  
npx expo start  

---

## 🔌 Ports Summary

XRPL Service → 3001  
Backend API → 8000  
Expo → 19000  

---

## 🧑‍🤝‍🧑 Git Workflow

- main → stable
- dev → integration
- feature branches → feature/your-name

---

## ❗ Common Issues

- Port already in use → stop old process
- Mobile cannot reach API → use local IP instead of localhost
- Expo stuck → run `npx expo start -c`