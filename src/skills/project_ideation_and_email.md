---
name: internship-cold-outreach
description: End-to-end workflow for Kushagra Agarwal's software-engineering internship applications. Given a target company and role, it researches the company's engineering priorities, finds the gap between them and his resume, proposes 1-2 original (non-clone) projects built around a technology the company values, writes the matching resume bullet, and drafts a unique, short, high-signal cold email to a recruiter or engineer. Use this skill whenever the user names a company and/or role and wants a cold email, outreach message, referral ask, follow-up, resume tailoring, "what project should I build for X", or help applying for an internship or SDE role, even if they only say something like "now do Razorpay, SDE intern" or "personalise the email for Atlassian".
---

# Internship Cold Outreach (research → project → resume bullet → email)

## Why this skill exists

A generic resume and a generic email get ignored. Hiring teams skim for about 30 seconds, and engineers in particular distrust vague claims and respond to specifics: a concrete technical problem, a real number, a decision explained. This skill makes every output specific to one company, honest about what the candidate has actually built, and short enough to read on a phone. Follow the phases in order and do not skip the gates. They exist because skipping them is how emails become generic or claim things that are not true.

## Candidate profile (source of truth)

All claims in any output must come from this section or from something the user tells you in the conversation. Never invent metrics, employers, tools, or project details. If a detail is missing, ask or leave a clearly marked `[slot]`.

**Identity:** Kushagra Agarwal, B.Tech IT (Integrated Dual-Degree), IIIT Gwalior, Aug 2023 - May 2028, CGPA 7.50. Phone +91-8604967161, email kushagraagarwal1612@gmail.com. Links: LinkedIn, GitHub, LeetCode, Codeforces, CodeChef (use the real URLs if the user supplies them; otherwise keep the link labels).
**Target timing:** Summer 2027 internship, "pre-final-year". Confirm with the user once per conversation if it is unclear.

**Proof-point bank** (pick from these; do not embellish):

| ID | Proof | Good for |
|---|---|---|
| EXP-1 | Increff SWE intern (Jan-Mar 2026): Redis cache-aside layer + PostgreSQL connection pooling cut API latency 40% across 300+ concurrent sessions; RBAC and modular Node/Express REST APIs (SOLID) serving 5,000+ users | Almost every backend role. Default Proof 1 |
| PRJ-LSM | LSM-tree storage engine in C++: skip-list memtable, Bloom filters, block-indexed SSTables, leveled and size-tiered compaction benchmarks, WAL with crash recovery validated over hundreds of `kill -9` injections, ASan in CI | Databases, storage, infra, systems, fintech, trading |
| PRJ-RAG | Hybrid RAG pipeline: pgvector dense search + BM25, Reciprocal Rank Fusion, reranking, cost-aware routing, tenant-aware Redis semantic cache, 100-query labeled eval set, 50+ edge cases | AI products, search, LLM tooling |
| PRJ-CRDT | Real-time collaborative whiteboard: hand-built CRDTs, Lamport clocks, fractional indexing, offline outbox, WebSockets, op-log + PostgreSQL snapshots, chaos testing | Real-time, collaboration, sync, distributed systems |
| WIN-1 | Won Monad Blitz Hackathon (New Delhi, Mar 2026): full product shipped in Python in 6 hours (ask the user what it was before using) | Startups, product-heavy teams |
| WIN-2 | HackVega 2.0 finalist (48,000+ participants); ATF Fellowship 2025 National Finalist (top 500 of 100,000+) | Supporting credibility only |
| CP | Codeforces Expert (max 1790), CodeChef peak 1869 (4-star), 600+ LeetCode problems | Companies that screen on algorithms |
| LEAD | Directed Infotsav 2025 (1,500 participants, 100+ volunteers); led 37-member Uthaan Club team | Rarely. Only for culture/ownership-focused roles |

**Stack:** C/C++, Python, JavaScript, TypeScript, SQL; Node/Express, React, Next.js, REST, WebSockets; PostgreSQL, MySQL, MongoDB, Redis, pgvector; Linux, Docker, Git, CI/CD, CMake, ASan.

## Inputs to collect (Phase 0)

Required: company, role title. Strongly useful: job ID or JD link, recipient name/title, referral or connection, whether he has already applied, how many weeks he can spend on a new project, anything he personally likes about the company.

If company and role are both present, start working immediately (research needs no further input) and ask for missing optional items alongside the first results. If the company is missing, ask for it and nothing else. If several companies are given, run the full workflow for each one separately and sequentially. Never reuse a "why them" paragraph or project idea across companies.

## Phase 1: Company research (ground everything)

Use WebSearch and WebFetch. Fetch the JD itself if a link is given. Gather:

1. **Role requirements:** stack, keywords, seniority signals, any emphasis (reliability, scale, AI use, ownership).
2. **What the company's engineering actually cares about:** engineering blog posts, tech talks, open-source repos, careers page values, recent launches. Prefer primary sources over aggregators.
3. **One concrete, verifiable technical hook** that could open the email (a specific system, problem, or blog post). Record the source URL.
4. **People:** if the user wants a named recipient, look for the relevant recruiter or engineering manager via public pages only. Do not guess or scrape private emails. Suggest the user find the address themselves via LinkedIn or the company's published format.

Gate: you must be able to state, in one sentence, "this company's engineering is hard because ___". If you cannot find this from sources, say so plainly and ask the user for the JD instead of writing a generic reason. Do not fabricate company facts. Current facts (products, scale, tech stack) must come from a search, not memory. Keep any quoted source text under 15 words; paraphrase otherwise.

## Phase 2: Fit and gap analysis

Make a short internal table of the company's top 3-5 technical themes against the proof-point bank.

- **Strong match:** a bank item directly demonstrates the theme. Use it.
- **Partial match:** an item touches the theme. Use it, and frame the transferable part honestly.
- **Gap:** nothing in the bank demonstrates a theme that matters to the role. This is what a new project should fill.

Report the result to the user in two or three lines. Do not dump the full table unless asked.

## Phase 3: Project proposals (only when there is a gap, or the user asked)

Propose **two** options, ranked, each following these constraints:

- **Not a clone.** Never replicate the company's product (no "a mini Stripe"). Build a component or study around a *technology or problem class* the company prioritizes, such as an idempotent ledger, an oversell-proof reservation service, or an LLM gateway with eval harness.
- **Built on something he already has** where possible (extend the LSM engine, the CRDT whiteboard, or the RAG pipeline), because depth beats breadth and it shortens the build.
- **Scoped to 1-3 weeks** (ask for his time budget; default 2 weeks).
- Contains **one hard technical decision**, **one measurable result** (benchmark, p99, convergence under failure, eval score), and **one failure test** (crash, partition, load, adversarial input).
- Uses the company's technologies or close equivalents where the license and his skills allow.

For each option provide: name; the company priority it targets (cite the Phase 1 evidence); core design in 3-5 lines; week-by-week outline; what to measure; the "what I'd do next" angle for interviews; and the **draft resume bullet** (see Phase 4). Make the options meaningfully different (e.g. one systems-flavored, one product-flavored).

Then state the honesty rule explicitly to the user: the project goes on the resume and into the email only after it runs and has real numbers.

## Phase 4: Resume bullet(s)

Write bullets in his existing resume format: one line of action + technique + measured outcome, past tense, quantified, no filler adjectives. Pattern: `Verb + what you built + using specific technique/tools, achieving measured result.` For a not-yet-built project, write the bullet with `[X]` placeholders for numbers and label it **DRAFT, fill after measuring**. Suggest which existing bullet to demote or drop to keep the resume to one page. Do not edit his resume file unless asked.

## Phase 5: Email drafting

Produce **two versions** when a new project is proposed, otherwise one:

- **Version A (send now):** uses only existing proof points.
- **Version B (send after the project is built):** swaps in the new project as Proof 2. Mark clearly that it must not be sent until the project is real.

### Email structure (fixed)

**Subject** (about 40 characters, specific, no clickbait): `[Role] Intern, Summer 2027 | IIIT Gwalior | [≤6-word hook]`

**Body, 90-140 words, short paragraphs, plain text:**

1. **Greeting + identity + ask.** Named recipient if known, else "[Company] Recruiting Team". Name, year, college, role (+ job ID), Summer 2027. One sentence.
2. **Why them.** 1-2 sentences naming the specific technical problem from Phase 1, tied to something he has built. Must be impossible to paste into another company's email unchanged.
3. **Proof 1.** EXP-1 by default (or the strongest fit), with its number.
4. **Proof 2.** The best-matching project from the bank, or Version B's new project: what, one technical decision, one result.
5. **Ask + resume.** "I've attached my resume. Would you be open to ___?" One concrete, low-friction ask. Offer to walk through Proof 2.
6. **Signature.** Name, phone, college, links (LinkedIn | GitHub | LeetCode | Codeforces Expert 1790).

### Writing rules

- Plain, direct, confident. No "passionate", "hardworking", "I would love to learn", "kindly consider", or flattery about the company's greatness.
- Output, not adjectives: "built X that did Y" beats "interested in X".
- Mirror 2-3 keywords from the JD naturally; do not keyword-stuff.
- Each proof point is one sentence with one number. No list of three projects.
- If a referral exists, mention it in the first line and the subject.
- If he has already applied, mention the job ID so it can be matched.
- Never bcc a batch. One email, one recipient, one company.
- The email must stay accurate against the profile. Run the checklist in Phase 6 before showing it.

### Alternate recipients

- **Recruiter:** lead with role fit and application ID; keep technical depth to one detail.
- **Engineer or manager:** lead with the technical hook; include one sentence they could reply to technically, and a smaller ask (a 10-minute chat or feedback on a design).
- **Founder at a startup:** shortest version, lead with what he can ship, mention WIN-1 if applicable.

## Phase 6: Quality gate (run silently before delivering)

Check every item. Fix failures rather than reporting them, unless a fix needs user input.

- [ ] Every number and claim traces to the profile or the user's words
- [ ] The "why them" line cites something specific and sourced from Phase 1
- [ ] Body is 90-140 words (count them)
- [ ] Exactly one ask
- [ ] Subject is specific and about 40 characters
- [ ] No clichés or banned phrases listed above
- [ ] Not reusing wording from a previous company's email in this conversation
- [ ] Version B is clearly labelled "do not send until built"
- [ ] No typos, consistent capitalization, correct company and role names
- [ ] Project proposals are not clones and each includes a failure test and a measurable result

## Phase 7: Delivery format

Reply in this order, keeping the whole response skimmable:

1. **Research snapshot** (3-5 lines): what the company prioritizes, the hook, and sources as a short "Sources:" list of links.
2. **Fit and gap** (2-3 lines).
3. **Project options** (if applicable), each with outline and draft resume bullet.
4. **Email(s)**: subject and body in a code block or clear block so they can be copied. Version A first, then Version B.
5. **Send plan** (2-3 lines): send Tuesday to Thursday, one follow-up after 5-7 days. Offer to draft that follow-up.

If the user asks for a file, write the deliverable as a Markdown or Docs document. Otherwise answer in the conversation.

## Follow-up email (when asked or after 5-7 days of no reply)

2-4 sentences. Reply on the same thread. Add one new piece of value (a new commit, a benchmark result, a shipped project), restate the ask in one line, and thank them. Never guilt-trip or say "just bumping this".

## Edge cases

- **JD not public or login-walled:** ask the user to paste it. Do not guess requirements.
- **Company with no engineering blog:** use the careers page, the product's public behavior, and open-source repos; say the evidence is thinner.
- **No relevant gap:** skip Phase 3 and say the current resume already fits; spend the effort on the email.
- **User wants to add a project to the resume right away:** remind them it should be built first; offer the draft bullet with placeholders.
- **Non-software roles or full-time roles:** adapt the subject and the ask, keep all other rules.
- **Conflicting information about the company:** report the conflict and which source you trust more.
- **User pushes back on length:** shorten by removing Proof 2 before removing "why them".

## Anti-patterns (never do these)

- Cloning the company's product as the project idea
- Claiming an unbuilt project as done
- Pasting the same paragraph into emails for different companies
- Listing every project and skill from the resume
- Inventing company facts, recipient names, or email addresses
- Long, multi-ask emails over about 140 words
- Using more than one quote from a single source, or quotes of 15 or more words

## Example (shape only)

**Input:** "Company: Razorpay, role: SDE Intern, I applied last week, job ID 12345."
**Behaviour:** research Razorpay engineering priorities (for example payment correctness and idempotency, from their blog or JD). Gap: no payments-correctness proof. Propose a double-entry ledger service with idempotency keys and an outbox-based webhook system, plus property tests and a reconciliation job. Draft Version A with EXP-1 + PRJ-LSM (durability angle), and Version B swapping in the ledger project once it is built.
