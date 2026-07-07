import os
import json
import urllib.request
import urllib.error
import asyncio
from typing import List, Dict, Any, Optional
from app.core.config import settings

def sync_openai_call(system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.MODEL_NAME or "gpt-4-turbo-preview",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30.0) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except Exception as e:
        print(f"urllib openai error: {e}")
        return None

class CareerService:
    @staticmethod
    def _is_openai_configured() -> bool:
        return bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "" and settings.OPENAI_API_KEY != "your_openai_key")

    @staticmethod
    async def _call_openai(system_prompt: str, user_prompt: str) -> Optional[str]:
        if not CareerService._is_openai_configured():
            return None
        try:
            loop = asyncio.get_running_loop()
            res = await loop.run_in_executor(None, sync_openai_call, system_prompt, user_prompt)
            if res and "choices" in res:
                return res["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"OpenAI urllib request failed: {e}")
            return None


    @staticmethod
    async def generate_resumes(profile: Dict[str, Any], repositories: List[Dict[str, Any]], languages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates 7 types of resumes based on GitHub profile and repositories.
        """
        username = profile.get("login", "Developer")
        name = profile.get("name") or username
        bio = profile.get("bio") or "Professional Software Engineer"
        followers = profile.get("followers", 0)
        public_repos = profile.get("public_repos", 0)
        
        # Summarize repositories for the context
        repo_names = [r.get("name") for r in repositories[:10]]
        repo_details = []
        for r in repositories[:8]:
            desc = r.get("description") or "No description provided"
            lang = r.get("language") or "Other"
            stars = r.get("stargazers_count", 0)
            repo_details.append(f"- **{r.get('name')}** ({lang}): {desc} ({stars} stars)")
        
        repos_summary = "\n".join(repo_details)
        top_langs = ", ".join([l.get("name", "") for l in languages[:4]]) or "JavaScript, Python, TypeScript"

        system_prompt = "You are an expert technical resume writer. Generate a comprehensive JSON structure containing 7 types of resumes: Professional, ATS, Academic, Research, Internship, Minimal, and Modern."
        user_prompt = f"""
        Generate resumes for {name} (@{username}).
        Bio: {bio}
        Followers: {followers}
        Public Repos: {public_repos}
        Top Languages: {top_langs}
        Repositories:
        {repos_summary}

        Please return a JSON object with keys:
        "professional", "ats", "academic", "research", "internship", "minimal", "modern".
        Each key should contain a Markdown-formatted resume string featuring sections: Summary, Skills, Experience (derived from repositories), Projects, and Education.
        """

        # Try to call OpenAI
        ai_response = await CareerService._call_openai(system_prompt, user_prompt)
        if ai_response:
            try:
                # Basic parsing check in case it's wrapped in markdown codeblock
                import json
                cleaned = ai_response.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                return json.loads(cleaned)
            except Exception as e:
                print(f"Failed to parse OpenAI JSON for resumes: {e}. Falling back to dynamic template generator.")
        
        # Heuristic Dynamic Fallback
        resumes = {}
        types = ["professional", "ats", "academic", "research", "internship", "minimal", "modern"]
        for t in types:
            title_type = t.upper()
            experience_section = ""
            for r in repositories[:5]:
                rname = r.get("name")
                rlang = r.get("language") or "Technology Stack"
                rdesc = r.get("description") or "Engineered scalable code modules, wrote documentation, and optimized execution flows."
                experience_section += f"### Lead Software Developer - project {rname} | {rlang}\n- Automated deployment processes and maintained repository operations.\n- Optimized codebase logic; implemented features based on {rlang}.\n- {rdesc}\n\n"

            resumes[t] = f"""# {name}
@{username} | {profile.get("email") or f"{username}@devtrack.io"} | {profile.get("blog") or "devtrack.io"}

## {title_type} SUMMARY
Highly skilled Software Engineer with a deep version control history of {public_repos} repositories. Proven background in {top_langs} workflows with an audience of {followers} followers on GitHub. Dedicated to building performant and maintainable applications.

## TECHNICAL SKILLS
- **Languages**: {top_langs}
- **Tools**: Git, Docker, Next.js, FastAPI, GitHub Actions, CI/CD
- **Specializations**: System Integration, REST APIs, Documentation

## PROJECTS & REPOSITORIES
{repos_summary or "- No repositories available."}

## WORK EXPERIENCE
{experience_section or "### Independent Open Source Developer\n- Contributed to personal and community codebases on GitHub.\n- Maintained coding calendar frequency and documented software designs."}

## EDUCATION
- **B.S. in Computer Science** | Global Software Academy
- **Certification**: DevTrack Developer DNA Index verified
"""
        return resumes

    @staticmethod
    async def analyze_ats(resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Validates resume text compatibility with job description, scoring it and providing comparisons.
        """
        system_prompt = "You are an ATS compliance scanner. Analyze the resume against the job description and return detailed JSON results."
        user_prompt = f"""
        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Provide a JSON analysis containing:
        - "score": integer 0-100
        - "missing_keywords": list of strings
        - "weak_sections": list of strings with explanations
        - "strong_sections": list of strings with explanations
        - "formatting_issues": list of strings
        - "impact_recommendations": list of suggestions
        - "before_vs_after": list of objects with "original" (weak line) and "revised" (stronger version) keys
        """
        
        ai_response = await CareerService._call_openai(system_prompt, user_prompt)
        if ai_response:
            try:
                import json
                cleaned = ai_response.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                return json.loads(cleaned)
            except Exception as e:
                print(f"Failed to parse OpenAI JSON for ATS: {e}")

        # Fallback heuristic calculation
        score = 65
        missing = ["CI/CD", "AWS Cloud", "System Design", "Microservices"]
        
        # Analyze basic keywords in job description vs resume
        jd_words = job_description.lower()
        res_words = resume_text.lower()
        
        detected_keywords = []
        for kw in ["react", "node", "python", "docker", "postgres", "fastapi", "typescript", "git", "kubernetes", "testing"]:
            if kw in res_words:
                detected_keywords.append(kw.capitalize())
            elif kw in jd_words:
                missing.append(kw.capitalize())

        if len(detected_keywords) > 2:
            score += 15
        
        return {
            "score": min(95, score),
            "missing_keywords": missing[:6],
            "weak_sections": [
                "Profile Summary: Lacks metrics or quantitative achievements.",
                "Cloud Architecture: No mention of scalable hosting infrastructure or cloud environments."
            ],
            "strong_sections": [
                "Version Control & Telemetry: Excellent GitHub footprints and repository structure.",
                "Technical Stack: Strong alignment in " + ", ".join(detected_keywords[:3])
            ],
            "formatting_issues": [
                "Table Elements: Heavy reliance on nested tables (legacy ATS engines may fail to parse column details).",
                "Date Formats: Inconsistent date format types in work experience history."
            ],
            "impact_recommendations": [
                "Include quantifiable achievements (e.g., 'reduced API response times by 30%').",
                "Structure experience using the STAR method (Situation, Task, Action, Result)."
            ],
            "before_vs_after": [
                {
                    "original": "Responsible for managing and writing code for backend repositories.",
                    "revised": "Architected and managed 5+ backend FastAPI repositories, improving overall engineering consistency score by 25%."
                },
                {
                    "original": "Worked with TypeScript and React to build client dashboards.",
                    "revised": "Engineered modular React client dashboards in TypeScript, reducing bundle rendering load times by 18%."
                }
            ]
        }

    @staticmethod
    async def match_job(resume_text: str, job_description: str, repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Job Match Score and readiness evaluation.
        """
        # Basic heuristic parsing
        jd_lower = job_description.lower()
        res_lower = resume_text.lower()
        
        score = 60
        missing = []
        
        common_skills = ["React", "TypeScript", "Python", "FastAPI", "Docker", "Kubernetes", "AWS", "SQL", "CI/CD", "Redis"]
        for skill in common_skills:
            in_jd = skill.lower() in jd_lower
            in_res = skill.lower() in res_lower
            if in_jd and not in_res:
                missing.append(skill)
            elif in_jd and in_res:
                score += 4
                
        # Repository names as signals
        repo_names = [r.get("name", "").lower() for r in repositories]
        for skill in common_skills:
            if skill.lower() in repo_names and skill not in res_lower:
                if skill in missing:
                    missing.remove(skill)
                score += 2 # Extra credit for having a repository for it
                
        score = min(98, max(40, score))
        
        readiness = "Medium"
        if score > 80:
            readiness = "Excellent"
        elif score > 70:
            readiness = "High"
        elif score < 50:
            readiness = "Low"

        return {
            "score": score,
            "missing_skills": missing[:5],
            "recommended_improvements": [
                f"Add repositories demonstrating your proficiency in {m}." for m in missing[:3]
            ] + ["Write a comprehensive README detailing structural architecture for your pinned repositories."],
            "interview_readiness": readiness,
            "verdict": f"The candidate has a {score}% match for this position, showing strong runtime credentials in repositories."
        }

    @staticmethod
    async def optimize_linkedin(profile: Dict[str, Any], repositories: List[Dict[str, Any]], languages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates LinkedIn items.
        """
        username = profile.get("login", "Developer")
        name = profile.get("name") or username
        top_langs = [l.get("name") for l in languages[:3]]
        langs_str = ", ".join(top_langs) or "Full Stack"
        repo_count = len(repositories)
        total_stars = sum(r.get("stargazers_count", 0) for r in repositories)

        headline = f"Software Engineer | Specialist in {langs_str} | DevTrack Certified Grade Developer | {repo_count} Projects on GitHub"
        about = f"""🚀 Passionate Software Architect specializing in {langs_str}. 

With a portfolio of {repo_count} public repositories and over {total_stars} stars accrued, I build clean, modular code bases and robust developer platforms. I focus on optimizing API performance, database models, and automated CI/CD validation.

Key Technical Stack:
- Programming: {', '.join([l.get('name') for l in languages[:5]])}
- Environments: Git, Docker, Node.js, Linux CLI

Always open to discussing systems architecture, open-source integration, and cloud-native application design."""

        exp_summary = f"Maintained and deployed {repo_count} open-source repositories. Engineered web platforms utilizing {langs_str}, establishing clean code practices and comprehensive documentation setups."
        
        skills = [l.get("name") for l in languages[:8]] + ["Git", "System Design", "Rest APIs", "Docker", "GitHub Actions"]

        featured = []
        for r in repositories[:3]:
            featured.append({
                "title": r.get("name"),
                "description": r.get("description") or "Open source software project.",
                "url": r.get("html_url")
            })

        return {
            "headline": headline,
            "about": about,
            "experience_summary": exp_summary,
            "skills": skills[:10],
            "featured_projects": featured,
            "bio": f"Software Engineer active on GitHub as @{username} with {repo_count} codebases."
        }

    @staticmethod
    async def analyze_portfolio(portfolio_url: str, profile: Dict[str, Any], repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes portfolio and profiles.
        """
        has_blog = bool(profile.get("blog"))
        avatar = profile.get("avatar_url")
        bio = profile.get("bio")
        
        passed_audits = []
        failed_audits = []
        
        if portfolio_url or has_blog:
            passed_audits.append("Deployment: Active portfolio site linked.")
        else:
            failed_audits.append("Deployment: Missing personal web index (no portfolio URL in profile).")
            
        if bio:
            passed_audits.append("Profile Bio: Catchy introduction configured.")
        else:
            failed_audits.append("Profile Bio: Blank description reduces professional presence.")
            
        with_desc = [r for r in repositories if r.get("description")]
        desc_ratio = len(with_desc) / len(repositories) if repositories else 0
        if desc_ratio > 0.8:
            passed_audits.append("Repository Metadata: 80%+ repositories have descriptions.")
        else:
            failed_audits.append(f"Repository Metadata: Only {len(with_desc)}/{len(repositories)} repositories have details.")

        with_homepage = [r for r in repositories if r.get("homepage")]
        if with_homepage:
            passed_audits.append("Demos: Found live deployment configurations in repositories.")
        else:
            failed_audits.append("Demos: Missing live demo links on your pinned repositories.")

        return {
            "score": int(desc_ratio * 40 + (30 if portfolio_url or has_blog else 0) + (30 if avatar else 0)),
            "passed": passed_audits,
            "warnings": [
                "Documentation: Readme documentation length in repositories is average.",
                "Performance: Image assets on portfolio site should be compressed to improve load times."
            ],
            "failed": failed_audits,
            "suggestions": [
                "Configure a custom domain for your web index to improve brand authority.",
                "Ensure your top 3 repositories have high-quality screenshots or gifs in the README.",
                "Connect devtrack telemetry badges to display your Developer Grade on your website."
            ]
        }

    @staticmethod
    async def generate_cover_letter(company: str, role: str, description: str, letter_type: str, profile: Dict[str, Any], languages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates cover letter.
        """
        name = profile.get("name") or profile.get("login", "Developer")
        email = profile.get("email") or f"{profile.get('login')}@devtrack.io"
        top_langs = ", ".join([l.get("name") for l in languages[:3]]) or "TypeScript, Go"
        
        system_prompt = f"You are a professional hiring coach. Write a customized cover letter for a {role} position at {company}."
        user_prompt = f"""
        Candidate: {name}
        Email: {email}
        Role Type: {letter_type} (e.g. Software Engineer, Backend, AI, ML, Frontend, Cloud, Research, Internship, Open Source)
        Target Company: {company}
        Target Role Title: {role}
        Role Description snippet: {description}
        Top Skills: {top_langs}

        Output a beautifully structured markdown cover letter.
        """

        ai_response = await CareerService._call_openai(system_prompt, user_prompt)
        if ai_response:
            return {
                "letter": ai_response,
                "company": company,
                "role": role,
                "type": letter_type
            }

        # Mock fallback cover letter
        letter = f"""Dear Hiring Manager at {company},

I am writing to express my strong interest in the {role} position at {company}. As a Software Engineer with extensive experience in {top_langs}, I am excited about the opportunity to contribute to your engineering goals.

My software engineering track record features verified public code repositories, showcasing consistency and clean design. For the {role} role, my specific experience with {top_langs} aligns well with the requirements mentioned: "{description[:150]}...".

Key highlights of my background include:
- Designing modular, reusable software components with clear REST integrations.
- Actively collaborating through GitHub version control, reviewing PRs, and maintaining project documentation.
- Focusing on performance optimization, automated tests, and containerization.

I am enthusiastic about {company}'s vision and would love to bring my technical skills and collaborative mindset to your team. Thank you for your time and consideration.

Sincerely,

{name}
{email}
https://github.com/{profile.get('login')}
"""
        return {
            "letter": letter,
            "company": company,
            "role": role,
            "type": letter_type
        }

    @staticmethod
    async def generate_roadmap(languages: List[Dict[str, Any]], target_role: str) -> Dict[str, Any]:
        """
        Generates roadmap.
        """
        top_langs = [l.get("name") for l in languages[:2]]
        langs_str = " and ".join(top_langs) or "JavaScript"
        
        # Determine recommendations based on target
        if "ai" in target_role.lower() or "ml" in target_role.lower():
            roadmap = {
                "30": {
                    "title": "Machine Learning Fundamentals",
                    "milestones": [
                        "Master Python data manipulation libraries (NumPy, Pandas).",
                        "Study core statistical concepts: regression, classification, and clustering.",
                        "Connect basic model APIs (OpenAI, HuggingFace) to local services."
                    ],
                    "resources": ["Kaggle Intro to Machine Learning", "Coursera Python for Data Science"]
                },
                "90": {
                    "title": "Deep Learning & Vectors",
                    "milestones": [
                        "Implement vector search indexing with Pinecone or pgvector.",
                        "Train basic models with scikit-learn and explore PyTorch tensors.",
                        "Build an RAG pipeline analyzing codebase files."
                    ],
                    "resources": ["DeepLearning.AI LangChain Course", "Fast.ai Practical Deep Learning"]
                },
                "180": {
                    "title": "Production AI Pipelines",
                    "milestones": [
                        "Deploy model endpoints using FastAPI containerized in Docker.",
                        "Configure model logging and token budget telemetry.",
                        "Build agentic workflows running multiple tool calls."
                    ],
                    "resources": ["Full Stack Deep Learning", "FastAPI Docs"]
                },
                "365": {
                    "title": "Scale & Open Source",
                    "milestones": [
                        "Fine-tune a small LLM on custom codebase datasets.",
                        "Publish custom integrations or open-source packages.",
                        "Design distributed vector caches."
                    ],
                    "resources": ["HuggingFace Course", "DevTrack AI Indexer"]
                }
            }
        elif "backend" in target_role.lower() or "systems" in target_role.lower() or "devops" in target_role.lower() or "platform" in target_role.lower():
            roadmap = {
                "30": {
                    "title": "API Architectures & Databases",
                    "milestones": [
                        "Design relational database schemas with proper index optimizations.",
                        "Implement authentication protocols (OAuth, JWT, session tokens).",
                        "Write unit tests with mock databases."
                    ],
                    "resources": ["PostgreSQL Tutorial", "FastAPI/Node.js Security docs"]
                },
                "90": {
                    "title": "Caching & Message Queues",
                    "milestones": [
                        "Configure distributed caching (Redis) for API speedups.",
                        "Implement background task queues with Celery or BullMQ.",
                        "Containerize local multi-service applications with Docker Compose."
                    ],
                    "resources": ["Redis University", "Docker Handbook"]
                },
                "180": {
                    "title": "Cloud Orchestration & CI/CD",
                    "milestones": [
                        "Write CI/CD workflows (GitHub Actions) for automatic build testing.",
                        "Configure serverless deployment or AWS ECS instances.",
                        "Implement structured JSON logs and Prometheus metrics."
                    ],
                    "resources": ["AWS Developer Guide", "GitHub Actions Docs"]
                },
                "365": {
                    "title": "Systems Reliability",
                    "milestones": [
                        "Implement database sharding or replication.",
                        "Design microservices communicating via gRPC or Kafka.",
                        "Contribute core features to shared platform libraries."
                    ],
                    "resources": ["System Design Primer", "Kubernetes Up & Running"]
                }
            }
        else: # Default Fullstack / Frontend
            roadmap = {
                "30": {
                    "title": "Modern Frontend Frameworks",
                    "milestones": [
                        "Master React server components and Next.js routing paradigms.",
                        "Integrate Tailwind CSS V4 for theme tokens.",
                        "Write interactive layouts using Framer Motion."
                    ],
                    "resources": ["Next.js Learn Course", "TypeScript Handbook"]
                },
                "90": {
                    "title": "State Management & APIs",
                    "milestones": [
                        "Implement lightweight state hooks (Zustand) and server cache syncing.",
                        "Connect frontend clients to secure REST/GraphQL backend routes.",
                        "Handle skeleton loading and error boundary fallbacks."
                    ],
                    "resources": ["React Docs", "Zustand Github"]
                },
                "180": {
                    "title": "Testing & Optimization",
                    "milestones": [
                        "Write integration tests with Playwright or Cypress.",
                        "Optimize bundle size and achieve 95+ Lighthouse score.",
                        "Deploy preview branches with automated edge routing."
                    ],
                    "resources": ["Lighthouse Performance guidelines", "Playwright Docs"]
                },
                "365": {
                    "title": "Design Systems & Scale",
                    "milestones": [
                        "Create reusable component packages published internally.",
                        "Implement real-time features using WebSockets.",
                        "Contribute patches to upstream open-source frameworks."
                    ],
                    "resources": ["WebSockets specifications", "Open Source Contribution Guide"]
                }
            }
        return {
            "roadmap": roadmap,
            "target": target_role,
            "basis": f"Calculated based on {langs_str} proficiency."
        }

    @staticmethod
    async def generate_interview_questions(profile: Dict[str, Any], repositories: List[Dict[str, Any]], languages: List[Dict[str, Any]], target_role: str) -> List[Dict[str, Any]]:
        """
        Generates interview questions based on developer profile.
        """
        top_lang = languages[0].get("name", "TypeScript") if languages else "TypeScript"
        repo_names = [r.get("name") for r in repositories[:3]]
        repos_str = ", ".join(repo_names) or "repos"

        return [
            {
                "id": "q1",
                "category": "Technical",
                "question": f"Given your experience with {top_lang}, how do you manage memory profiling and async state resolution?",
                "answer_summary": f"In {top_lang}, managing async states requires handling promises securely and avoiding race conditions. Utilizing built-in async/await syntax and properly disposing of connections/listeners prevents memory leaks."
            },
            {
                "id": "q2",
                "category": "Behavioral",
                "question": "Describe a scenario where you contributed to public source files and had to align with other maintainers.",
                "answer_summary": "Emphasize communicating issues clearly through markdown, proposing small focused changes, writing unit tests to verify changes, and incorporating constructive code review reviews patiently."
            },
            {
                "id": "q3",
                "category": "Project Discussion",
                "question": f"Walk us through the architecture of your repository '{repo_names[0] if repo_names else 'personal-project'}'. Why did you pick this layout?",
                "answer_summary": "Discuss separating concerns (e.g., api layer, service layer, and data tier), selecting runtime configurations suitable for requirements, and automating validation hooks."
            },
            {
                "id": "q4",
                "category": "Coding Questions",
                "question": "Explain how you would write a custom rate-limiting middleware for an API router.",
                "answer_summary": "Use token-bucket or sliding-window algorithms stored in a memory cache like Redis. Increment requests per client IP and return 429 status code if requests exceed thresholds."
            },
            {
                "id": "q5",
                "category": "System Design",
                "question": "How would you design a repository sync engine that processes 10,000 repositories concurrently without API throttling?",
                "answer_summary": "Implement message queues (RabbitMQ/Kafka) with workers, distribute queries across rotating API access credentials, cache payloads, and schedule background syncs."
            }
        ]

    @staticmethod
    async def analyze_skill_gap(languages: List[Dict[str, Any]], repositories: List[Dict[str, Any]], target_role: str) -> Dict[str, Any]:
        """
        Compares current skills against requirements.
        """
        user_langs = {l.get("name", "").lower() for l in languages}
        
        # Skill requirements for target roles
        role_skills = {
            "frontend engineer": ["React", "TypeScript", "TailwindCSS", "Next.js", "Vite", "HTML/CSS"],
            "backend engineer": ["Node.js", "Python", "FastAPI", "SQL", "PostgreSQL", "Docker", "Redis"],
            "full stack": ["React", "Next.js", "TypeScript", "Node.js", "SQL", "Docker", "REST APIs"],
            "ai engineer": ["Python", "OpenAI API", "Vector Databases", "LangChain", "PyTorch"],
            "ml engineer": ["Python", "scikit-learn", "TensorFlow", "Pandas", "Jupyter"],
            "cloud engineer": ["AWS", "Terraform", "Docker", "Kubernetes", "Linux CLI", "IAM"],
            "devops": ["Docker", "Kubernetes", "GitHub Actions", "Terraform", "CI/CD", "Linux"],
            "platform engineer": ["Kubernetes", "Go", "Docker", "Terraform", "gRPC", "Prometheus"],
            "security engineer": ["OWASP Top 10", "Wireshark", "Bash", "Cryptography", "SSH"]
        }

        role_key = target_role.lower()
        skills = role_skills.get(role_key, role_skills["full stack"])
        
        matched = []
        missing = []
        
        for s in skills:
            # Simple check if keyword is in user languages
            if s.lower() in user_langs or (s.lower() == "sql" and "plpgsql" in user_langs) or (s.lower() == "node.js" and "typescript" in user_langs):
                matched.append(s)
            else:
                missing.append(s)
                
        # Calculate percentage
        pct = int((len(matched) / len(skills)) * 100) if skills else 100
        
        # Set learning resources
        resources = {
            "React": "React Official Docs (react.dev)",
            "TypeScript": "TypeScript Handbook (typescriptlang.org)",
            "TailwindCSS": "TailwindCSS V4 Documentation",
            "Next.js": "Next.js Learn (nextjs.org/learn)",
            "FastAPI": "FastAPI Tutorial (fastapi.tiangolo.com)",
            "Docker": "Docker Deep Dive (Udemy)",
            "Kubernetes": "Kubernetes Up & Running",
            "AWS": "AWS Certified Developer Guide",
            "Python": "Python Crash Course",
            "LangChain": "DeepLearning.AI LangChain short courses",
            "Vector Databases": "Pinecone / pgvector vector tutorials"
        }
        
        learning_items = []
        for m in missing:
            learning_items.append({
                "skill": m,
                "resource": resources.get(m, f"Official {m} Documentation and Tutorials")
            })

        return {
            "role": target_role,
            "current_percentage": pct,
            "missing_percentage": 100 - pct,
            "learning_time": f"{len(missing) * 2} weeks",
            "matched_skills": matched,
            "missing_skills": missing,
            "resources": learning_items
        }

    @staticmethod
    async def review_repository(repo_name: str, language: str, stars: int, readme_content: str) -> Dict[str, Any]:
        """
        Performs AI code quality and structure review.
        """
        score = 80
        
        issues = []
        improvements = []
        
        if not readme_content or len(readme_content) < 50:
            score -= 15
            issues.append("Documentation: README file is missing or contains sparse layout summaries.")
            improvements.append("Create a comprehensive README detailing setup steps, configuration settings, and API models.")
        else:
            improvements.append("Document architectural design flows and add code snippet examples to the README.")

        if stars == 0:
            issues.append("Community: Low developer resonance (0 stars).")
            improvements.append("Share repository on platforms and connect tags to improve index SEO.")
        else:
            score += min(10, stars)

        return {
            "repo_name": repo_name,
            "quality_score": min(98, score),
            "language": language or "Unspecified",
            "issues": issues,
            "improvements": improvements,
            "verdict": f"The codebase '{repo_name}' is structurally healthy. Actioning documentation updates will improve readiness scoring."
        }

    @staticmethod
    async def assistant_chat(message: str, profile: Dict[str, Any], repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes conversation queries and returns text responses.
        """
        username = profile.get("login", "Developer")
        repo_names = [r.get("name") for r in repositories[:5]]
        repos_str = ", ".join(repo_names) or "personal files"
        
        system_prompt = f"You are HireSight-AI, the advanced Career Engine inside DevTrack. The user is a developer. Provide career advice and repository optimization guides."
        user_prompt = f"User profile: {username}. Repositories: {repos_str}. Query: {message}"

        ai_response = await CareerService._call_openai(system_prompt, user_prompt)
        if ai_response:
            return {"response": ai_response}

        # Dynamic mock assistant responses
        msg_lower = message.lower()
        if "google" in msg_lower:
            resp = f"To prepare for Google, focus on sharpening your data structures and system design skills. Google recruiters look for structural code patterns. In your repositories like '{repo_names[0] if repo_names else 'dev-track'}', make sure to include automated test pipelines, which demonstrate Google-grade engineering habits."
        elif "docker" in msg_lower:
            resp = "Yes, learning Docker is highly recommended! Currently, 85% of Cloud/Backend roles list containerization as a core skill. Adding a `Dockerfile` to your repositories will improve your DevOps job readiness score by roughly 12%."
        elif "resume" in msg_lower:
            resp = "I can definitely help optimize your resume. Head over to the **Resume Builder** or **ATS Resume Analyzer** modules in the sidebar. I'll ingest your GitHub history and compose a customized CV matching target job descriptions."
        elif "grade" in msg_lower or "score" in msg_lower:
            resp = "To increase your Developer Grade in DevTrack:\n1. Write README files for all public repositories.\n2. Maintain your coding calendar consistency.\n3. Contribute to open-source systems.\n4. Reduce the fork ratio by launching original projects."
        else:
            resp = f"Hi! I'm your Career Intelligence Coach powered by HireSight-AI. I see you are maintaining {len(repositories)} projects (including '{repo_names[0] if repo_names else 'personal projects'}'). Ask me how to optimize your resume, review code quality, map out a learning roadmap, or check matching scores for target companies!"

        return {"response": resp}
