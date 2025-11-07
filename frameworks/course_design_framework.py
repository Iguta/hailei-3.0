"""Utility module that stores an example HAILEI course design summary template.

This template mirrors the educator-facing summary that the design_summary_task
should produce after all specialist agents (IPDAi, CAuthAi, TFDAi, EditorAi,
EthosAi, SearchAi) have completed their work. It is intended purely as a
reference/example and is not programmatically consumed elsewhere.
"""

EXAMPLE_COURSE_DESIGN_SUMMARY = """\
HAILEI Course Design Summary
Course Title: Foundations of Data Analytics
Credits / Duration / Level: 3 credits · 12 weeks · Graduate – Introductory

Course Overview
This course introduces core data analytics concepts—data wrangling, exploratory analysis,
basic statistical inference, and communicating insights. Learners gain practical fluency
with Python libraries (pandas, NumPy, Matplotlib) through real-world datasets. By the end,
students can clean, analyze, and visualize data responsibly, and explain their findings to
technical and non-technical audiences.

Learning Outcomes
- Terminal Learning Objectives (TLOs):
  1. Plan and execute an end-to-end data analytics workflow (Create).
  2. Interpret statistical results and articulate actionable recommendations (Evaluate).
- Sample Enabling Learning Objectives (ELOs):
  - For TLO 1:
    - Prepare raw datasets by applying data-cleaning and transformation steps in pandas (Apply).
    - Design reproducible notebooks documenting assumptions, code, and decisions (Create).
  - For TLO 2:
    - Distinguish between correlation and causation when evaluating findings (Analyze).
    - Compose executive-ready summaries that highlight risks, caveats, and implications (Evaluate).

Weekly Plan (12 Weeks – Highlights)
Week | Theme | Key Activities | Assessments | PRRR Signals
1 | Data Analytics Foundations | Lecture: analytics lifecycle; Lab: Jupyter basics | Diagnostic quiz | Personal (goal-setting reflection)
4 | Exploratory Data Analysis | Lab: pandas profiling; Discussion: bias in datasets | EDA report (individual) | Relatable (case: public health data)
7 | Inferential Thinking | Workshop: hypothesis design; Readings: ethics in inference | Mini project: A/B testing | Relative (peer review of analyses)
10 | Communicating Insights | Studio: slide decks; Guest AMA with industry analyst | Storyboard for final capstone | Real-world (industry mentor feedback)
12 | Capstone Delivery | Final presentations; Panel critique | Capstone project submission | All PRRR dimensions

KDKA Alignment (IPDAi)
- Knowledge: Core analytics concepts, statistical reasoning, data ethics.
- Delivery: Lectures, experiential labs, workshops, guest sessions.
- Context: Cross-industry case studies (public health, finance, civic analytics).
- Assessment: Weekly labs, EDA report, peer reviews, capstone project.

PRRR Integration
- Personal: Learners set individual goals and reflect weekly on skill growth.
- Relatable: Cases drawn from learners’ professional domains; collaborative analysis.
- Relative: Scaffolded projects build toward a final capstone, emphasizing incremental mastery.
- Real-world: Authentic datasets, stakeholder briefs, industry mentor feedback.

LMS Implementation (TFDAi)
- Platform: Canvas
- Structure:
  - Home page with course roadmap and “Getting Started” orientation.
  - Weekly modules with consistent pattern: overview → learning objectives → materials → assignments → reflections.
  - Interactive labs embedded via JupyterHub/LTI integration.
- Integrations:
  - Python (JupyterHub), Slack (peer collaboration), Zoom (guest speakers), Google Drive (shared datasets).
- Accessibility Notes:
  - Alt-text on visuals, transcripts for videos, accessible color palette in templates, high-contrast charts, screen-reader-optimized navigation.

Editorial Enhancements (EditorAi)
- Tone & Clarity: Harmonized language across modules; redundant instructions removed.
- Accessibility: Verified UDL checkpoints (multiple means of representation/expression/engagement).
- Bloom Alignment: Objectives tagged with cognitive levels; rubrics updated to evaluate higher-order thinking.
- Change Log: Provided to coordinator, detailing grammar fixes, accessibility adjustments, and rubric tweaks.

Ethical Audit (EthosAi)
- Compliance: Pass.
- Highlights:
  - Case studies vetted for diverse perspectives and inclusive datasets.
  - Data privacy topics integrated into Week 5 and Week 9.
  - Explicit guidance on responsible AI usage, bias mitigation, and stakeholder communication.
- Recommendations: Continue updating datasets annually to avoid outdated or non-inclusive examples.

Resource Curation (SearchAi)
- Total curated artifacts: 12 (peer-reviewed, OER-friendly). Examples:
  - “Practical Statistics for Data Scientists” – O’Reilly chapter on exploratory analysis (URL).
  - “Ethics in Data Science” – Harvard Berkman Klein Center report (URL).
  - “Storytelling with Data – The Podcast” – Season 3 episode on narrative framing (URL).
  - Public NYC 311 Dataset Portal – Source for civic analytics capstone (URL).
- All resources are catalogued with relevance notes, usage rights, and dataset documentation in the SearchAi appendix.

Appendices (per-agent deliverables)
- Appendix A – Course Foundations (IPDAi): Full syllabus draft, Bloom-tagged objectives, 12-week module table, KDKA matrices.
- Appendix B – Instructional Content Pack (CAuthAi): Lecture outlines, lab notebooks, discussion prompts, assignments, rubrics.
- Appendix C – LMS Implementation Blueprint (TFDAi): Canvas module templates, navigation maps, integration checklist, QA plan.
- Appendix D – Editorial Report (EditorAi): Detailed revision log, accessibility compliance checklist, Bloom alignment summary.
- Appendix E – Ethical Compliance Certificate (EthosAi): Audit findings, risk mitigation notes, monitoring recommendations.
- Appendix F – Curated Resource Library (SearchAi): Annotated bibliography, persistent links, licensing information.
"""


def get_example_course_design_summary() -> str:
    """Return the example course design summary template as a string."""

    return EXAMPLE_COURSE_DESIGN_SUMMARY
