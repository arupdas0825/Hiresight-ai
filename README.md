# HireSight AI 🚀 (Full-Stack Version)

HireSight AI is a premium, production-ready SaaS AI Resume Analyzer. It features a complete Node.js/Express backend, full React/Tailwind frontend, PDF resume extraction, Dark/Light mode, and LocalStorage analysis history tracking.

## Architecture

- **Frontend**: React.js, Tailwind CSS (Glassmorphism, Dark/Light mode), Framer Motion (Animations).
- **Backend**: Node.js, Express.js, `pdf-parse` for resume upload extraction, and Groq API (LLaMA3-70b-8192) for strict JSON evaluations.

## Features Deep-Dive

1. **PDF Resume Parsing**: Upload a .pdf, the backend extracts text and auto-fills the textarea.
2. **AI Analysis Engine**: Compares resumes vs job descriptions and grades Match Score, ATS Score, Impact Score, and finds relevant keywords.
3. **History Panel**: Saves historical analyses to localStorage. Click to reload past reviews.
4. **Theme Toggle**: Switch between clean Light mode and sleek Dark mode. The state persists locally.
5. **Fluid UI/UX**: Over 20+ micro-interactions with Framer Motion and custom CSS (glowing buttons, staggered loading screens, circular SVG rings).

## Setup Instructions

### 1. Backend Setup

Open a terminal and navigate to the backend.

```bash
cd resume-iq/server
npm install
```

Create a `.env` file in the `server` directory:
```env
PORT=5000
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:
```bash
npm start
# Server will run on http://localhost:5000
```

### 2. Frontend Setup

Open a new terminal and navigate to the root directory for the client setup.

```bash
cd resume-iq/client
npm install
```

Start the React Development Server:
```bash
npm start
# App will run on http://localhost:3000
```

## Folder Structure

```
resume-iq/
├── client/                 # Frontend React App
│   ├── src/
│   │   ├── components/     # UI Components (Loader, ThemeToggle, FileUpload...)
│   │   ├── pages/          # Layout Pages (Home.js)
│   │   ├── services/       # Frontend API routes interacting with Node.js
│   │   ├── utils/          # Helpers (Scores, Theme state hook)
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css       # Tailwind config with Variables
│   ├── tailwind.config.js
│   └── package.json
├── server/                 # Backend Node.js/Express API
│   ├── controllers/        # analyzeController, uploadController
│   ├── routes/             # /api/analyze, /api/upload
│   ├── services/           # groqService
│   ├── utils/              # promptBuilder
│   ├── server.js
│   └── package.json
└── README.md
```

## API Testing

**Health Check endpoint:**  
`GET http://localhost:5000/health`

**Upload PDF endpoint (FormData):**  
`POST http://localhost:5000/api/upload` - Key: `resumePdf` -> `.pdf` File

**Analyze endpoint (JSON):**  
`POST http://localhost:5000/api/analyze` - Payload: `{ "resumeText": "...", "jobDescription": "..." }`
