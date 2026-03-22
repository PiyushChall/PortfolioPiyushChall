# ✳ Piyush Chall — AI Portfolio

A Claude-inspired portfolio with a real Gemini-powered AI chatbot, built with **FastAPI**.

---

## 🚀 Quick Setup

### 1. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your Gemini API key
```bash
cp .env.example .env
```
Open `.env` and replace `your_gemini_api_key_here` with your actual key.  
Get a **free** key at: https://aistudio.google.com/app/apikey

### 3. Run the server
```bash
uvicorn main:app --reload
```

Open http://localhost:8000 — done! 🎉

---

## 📁 Project Structure

```
portfolio/
├── public/
│   └── index.html      # The entire frontend (Claude-style UI)
├── main.py             # FastAPI server + Gemini proxy
├── requirements.txt    # Python dependencies
├── .env                # Your secret API key (never commit this!)
├── .env.example        # Template — safe to commit
├── .gitignore
└── README.md
```

---

## 🔒 How the API key stays safe

```
Visitor's browser  →  POST /api/chat  →  Your server  →  Gemini API
                       (no key needed)    (key lives here)
```

The `.env` file stays on your server only. The frontend talks to `/api/chat` — your own endpoint — never to Gemini directly.

---

## 🌐 Deploying

### Railway (easiest, free tier)
1. Push to GitHub
2. New Project → Deploy from GitHub repo
3. Add `GEMINI_API_KEY` in Railway's Variables dashboard
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Render (free tier)
1. Push to GitHub → New Web Service on Render
2. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add `GEMINI_API_KEY` in Environment Variables

### VPS / any Linux server
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
# Use screen or systemd to keep it running
```
