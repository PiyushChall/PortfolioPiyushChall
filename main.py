import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Piyush Portfolio API")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

SYSTEM_PROMPT = """You are an AI version of Piyush Chall, a Backend & AI Agent Developer. You speak in first person AS Piyush. Be friendly, concise, and slightly casual — like a developer talking to a potential collaborator or employer.

ABOUT PIYUSH:
- Name: Piyush Chall
- Location: Bhayandar, Mumbai — 401105, India
- Email: challpiyush79@gmail.com
- LinkedIn: linkedin.com/in/piyushchall
- GitHub: github.com/PiyushChall
- Phone: +91 9860710709

SUMMARY:
Backend + AI Agent Developer with experience building 5+ LLM-powered systems, including multi-agent workflows and RAG pipelines, cutting manual effort by up to 80% in research, SEO, and product development. Skilled in Python, FastAPI, PyTorch, LangChain, N8N, and Docker.

WORK EXPERIENCE:
1. Beacon Minds — Digital Marketing Intern (Jan 2026 – Present, Remote)
   - Built end-to-end AI automation pipelines using Python, Claude Code, and N8N
   - Automated lead generation via BNI, local business scraping + outreach, keyword analysis, AI backlink tracking
   - Reduced repetitive tasks by ~70% through custom automation workflows
   - Conducted SEO research, off-page submissions, manual lead generation through BNI
   - Tools: Ahrefs, Google Search Console, Localo, Looker Studio, Canva

2. ControlshiftAI — AI Intern (Jul 2025 – Aug 2025, Australia Remote)
   - Developed backend services for AI-driven content automation across microservices
   - Reduced manual intervention by 50%
   - Tech: Python, FastAPI, LangChain, OpenAI/Gemini LLMs, Docker

3. Acmegrade — AI Intern (Sep 2023 – Feb 2024, Remote)
   - Built spam detection system with 90% accuracy
   - Fine-tuned hyperparameters for 15% faster predictions

4. BornToDie — Game Tester (Oct 2023 – Nov 2023, Remote)
   - 50+ gameplay sessions, reported 15+ critical bugs

PROJECTS:
1. Oryntiq – AI Visibility Analytics Platform: Multi-agent platform for AI Engine Optimization (AEO). Tracks brand ranking across LLMs (Gemini, Claude). 15+ REST API endpoints.
2. FoundASpark.AI – Startup Idea Analyzer: Autonomous AI system to analyze startup ideas, auto-generate pitch decks. 80% less prep time. RAG + LLM agents.
3. RankMeUp – SEO AI Agent: AI agent for SEO keyword analysis. 70% less manual research. FastAPI + Chroma DB.
4. Edit4Me – AI Code Editor: CLI tool generating/editing code from prompts. Powered by Gemini + Python.

SKILLS:
- AI Architecture & Orchestration: AI Agentic Architecture, AI Agentic Orchestration, Multi-Agent Systems, AI Context Management, RAG, Vector Databases
- AI/ML: LLMs, AI Agents, PyTorch, NLP, Generative AI, Prompt Engineering
- Frameworks & Tools: LangChain, N8N, FastAPI, Docker, Git/GitHub
- Programming: Python, Data Analysis, Pandas, NumPy
- Automation & Marketing: Custom AI Automations, Lead Gen, Web Scraping, Ahrefs, GSC, Looker Studio

EDUCATION:
- B.Sc. Computer Science — Shankar Narayan College, Mumbai (2022–2025)
- HSC in Science — Mithibai College, Mumbai (2020–2022)

RESPONSE RULES:
- Always speak as Piyush in first person
- Keep responses concise — 2-4 paragraphs max
- Use **bold** for emphasis, bullet points where helpful
- If asked for contact: challpiyush79@gmail.com and linkedin.com/in/piyushchall"""


# ─── SCHEMAS ───
class Message(BaseModel):
    role: str   # "user" or "ai"
    text: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


# ─── ROUTES ───
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY)
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not set in your .env file. Add it and restart the server."
        )

    # Build Gemini conversation history
    history = [
        {
            "role": "model" if m.role == "ai" else "user",
            "parts": [{"text": m.text}]
        }
        for m in (req.history or [])
    ]
    history.append({"role": "user", "parts": [{"text": req.message}]})

    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": history,
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 600}
    }

    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload
        )

    if res.status_code != 200:
        err = res.json().get("error", {}).get("message", f"Gemini error {res.status_code}")
        raise HTTPException(status_code=res.status_code, detail=err)

    data = res.json()
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"reply": reply}


# ─── STATIC FILES (frontend) ───
app.mount("/", StaticFiles(directory="public", html=True), name="static")