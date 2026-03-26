<div align="center">
  <h1>🚀 HireSight AI</h1>
  <p><strong>A Premium, Full-Stack SaaS AI Resume Analyzer</strong></p>
  <a href="https://hiresight-ai-delta.vercel.app/" target="_blank"><strong>🔗 View Live Application</strong></a>
  <br />
  <br />
  <!-- Placeholder for a beautiful header screenshot -->
  <img src="https://via.placeholder.com/1000x500/0f172a/3b82f6?text=HireSight+AI+Dashboard" alt="HireSight AI Dashboard" width="100%" style="border-radius: 12px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);" />
</div>

<hr />

## 🌟 Overview

As a Senior Developer and Architect, I engineered **HireSight AI** to be a scalable, production-ready full-stack application. It leverages the power of Large Language Models (LLMs) to bridge the gap between candidate resumes and job descriptions. 

This isn't just a prototype—it is a **complete project** built entirely from the ground up with a custom Node.js/Express backend capable of memory-buffered PDF parsing, paired with a highly polished React frontend. We employ a modern semantic "Glassmorphism" UI system engineered for maximum layout stability and user engagement. By utilizing the free tier of the Groq API (powered by LLaMA3-70b), HireSight AI performs instantaneous, rigorous JSON evaluations.

## 📸 Interface Sneak Peek

<p align="center">
  <img src="https://via.placeholder.com/480x300/f8fafc/0f172a?text=PDF+Parsing+Upload+Module" alt="PDF Parsing" width="48%" />
  <img src="https://via.placeholder.com/480x300/1e293b/f8fafc?text=Sleek+Dark+Mode+UI" alt="Dark Mode UI" width="48%" />
  <br/>
  <em>State-of-the-Art Glassmorphism Input paired with seamless Dark/Light Mode.</em>
</p>

## 🏗️ Architecture Stack

- **Frontend**: React.js, Tailwind CSS (Custom Dark/Light mode integration), Framer Motion (Orchestrating micro-interactions).
- **Backend**: Node.js, Express.js, `pdf-parse` for multipart resume extraction without relying on temp files on disk.
- **AI Core**: Groq API (`llama3-70b-8192`) engineered via strict prompt-tuning to guarantee valid JSON outputs.
- **Deployment**: Vercel (Frontend & Serverless logic).

## ✨ Features Deep-Dive

1. **PDF Resume Parsing**: Upload a `.pdf` directly into the dropzone. The Node backend intercepts the buffer, extracts the raw text natively, and streams it back to auto-fill the React textarea.
2. **AI Analysis Engine**: Conducts deep semantic comparisons between the resume and target job descriptions. It deterministically calculates Match %, ATS %, Impact %, and highlights exactly which keywords are completely missing.
3. **Session History Panel**: Persists all historical analytics logic natively to the client's `localStorage`. Switch contexts seamlessly without hitting a traditional database.
4. **Theme Toggle**: Switch effortlessly between a pristine Light layout and a heavily engineered Dark mode (persisted automatically).
5. **Fluid UI/UX**: Over 20+ orchestrated micro-interactions. Magnetic animated loaders, staggered reveal states, and programmatic SVG radius scores.

## 🚀 Setup & Local Development

### 1. Backend Initialization

```bash
cd resume-iq/server
npm install
```

Create a `.env` file in the `server` directory and configure your Groq API credentials:
```env
PORT=5000
GROQ_API_KEY=your_groq_api_key_here
```

Spin up the RESTful service:
```bash
npm start
# Server boots up on http://localhost:5000
```

### 2. Frontend Initialization

Open a new terminal session and navigate to the client root:

```bash
cd resume-iq/client
npm install
```

Start the React Development Server:
```bash
npm start
# App hot-reloads on http://localhost:3000
```

## 📂 Monorepo Project Structure

```text
resume-iq/
├── client/                 # Progressive Web Application (React)
│   ├── src/
│   │   ├── components/     # Reusable UI Atoms and Molecules
│   │   ├── pages/          # Layout Orchestration
│   │   ├── services/       # Isomorphic API Abstraction Layer
│   │   ├── utils/          # Pure helper hooks
│   │   ├── App.js          # Root Component Tree
│   │   └── index.css       # Core Tailwind CSS & Custom Behaviors
│   └── package.json
├── server/                 # RESTful API Service (Node/Express)
│   ├── controllers/        # Request Handlers (analyze, upload)
│   ├── routes/             # Express Router Middleware
│   ├── services/           # Third-party Integrations (Groq logic)
│   ├── utils/              # Prompt Engineering & Validation
│   ├── server.js           # Express Bootstrap Execution
│   └── package.json
├── package.json            # Deployment proxy scripts for Vercel overrides
└── vercel.json             # Vercel infrastructure routing settings
```

## 📡 API Reference

**Health Check Validation:**  
`GET /health` (`200 OK`)

**PDF Buffer Upload Extraction (Multipart/FormData):**  
`POST /api/upload` - Expecting: `resumePdf` as a `.pdf` buffer.

**LLM Analysis Inference (JSON):**  
`POST /api/analyze` - Playload: `{ "resumeText": "...", "jobDescription": "..." }`

---
<div align="center">
  <p>Engineered with precision. Deployed for scale.</p>
</div>
