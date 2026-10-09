---
name: resume-optimizer
description: Skill for optimizing technical resumes for ATS systems and human recruiters. Covers the Google XYZ formula, STAR method bullet points, ATS-friendly formatting, keyword optimization, and quantified impact metrics for software engineering resumes.
---

# Resume Optimizer Skill

## Core Principles

### 1. Google's XYZ Formula for Every Bullet Point
**"Accomplished [X] as measured by [Y], by doing [Z]."**
- X = The accomplishment/outcome
- Y = The metric/measurement (%, $, time, users, performance)
- Z = The method/tools/approach used

### 2. ATS Optimization Rules
- **Single-column layout** — no tables for layout, no multi-column designs
- **Standard section headings**: Education, Experience, Projects, Skills, Achievements
- **No graphics, icons, or images** — ATS cannot parse them
- **No headers/footers** — ATS ignores them; put contact info in body
- **Text-based PDF** — not image-based
- **Standard fonts** — Latin Modern, Computer Modern, Arial, Calibri
- **Keywords must appear in BOTH** the Skills section AND within Experience bullet points (contextual placement)

### 3. Bullet Point Best Practices
- Start every bullet with a **strong, unique action verb** (never repeat the same verb)
- **Quantify everything**: latency, throughput, users, error rates, cost savings, team size, time saved
- **Bold the tech stack** within bullet points so human readers can scan
- Keep bullets to **1-2 lines max** — concise and scannable
- Use **3 bullets per role** (max 4 for most recent role)
- Avoid passive voice and duty-listing ("Responsible for...")
- Each bullet should answer: "So what? Why does this matter?"

### 4. Section Order (for students/early career)
1. Header (Name + Contact)
2. Education
3. Experience
4. Projects
5. Technical Skills
6. Achievements / Awards
7. Open Source (if applicable)

### 5. Strong Action Verbs (never repeat)
Tier 1 (High Impact): Architected, Engineered, Spearheaded, Pioneered, Orchestrated
Tier 2 (Technical): Implemented, Optimized, Automated, Refactored, Containerized
Tier 3 (Collaborative): Collaborated, Mentored, Led, Coordinated, Delivered
Tier 4 (Analytical): Analyzed, Benchmarked, Profiled, Diagnosed, Instrumented

### 6. Common Mistakes to Avoid
- Listing duties instead of achievements
- Using the same action verb repeatedly
- No metrics or quantification
- Overly long bullets that wrap to 3+ lines
- "Grocery listing" technologies without showing impact
- Using tables/columns that break ATS parsing
- Missing keywords from target job descriptions
- Using abbreviations without spelling them out first

### 7. Formatting Tips for LaTeX
- Use `\textbf{}` to bold tech stacks within bullets
- Keep consistent spacing between sections
- Ensure hyperlinks use `\href{}` with `hidelinks` option
- Verify the PDF is text-selectable (not rendered as images)
- Test with ATS parsers before submitting
