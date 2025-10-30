# HAILEI proprietary frameworks
KDKA_FRAMEWORK = {
    "summary": "KDKA aligns Knowledge, Delivery, Context, and Assessment so learning design centers the learner, not the teacher, and remains constructively aligned across modalities.",
    "pedagogical_basis": [
        "Learning is dynamic and contextual; design must connect content to learner needs.",
        "Delivery should span multiple modalities with accessibility in mind.",
        "Assessment must include formative and summative evidence aligned to outcomes."
    ],
    "how_to_use": "For each module, explicitly list target knowledge, choose delivery modes that fit learners and constraints, situate activities in authentic contexts, and align assessments to the stated outcomes.",
    "dimensions": {
        "knowledge": "Facts, concepts, skills, and metacognition tied to outcomes and Bloom levels.",
        "delivery": "Modalities and methods such as micro-lectures, labs, peer discussion, debates.",
        "context": "Authentic scenarios, stakeholders, constraints, and equity considerations.",
        "assessment": "Formative and summative checks aligned to outcomes; transparent criteria."
    },
    "ai_course_defaults": {
        "knowledge_examples": [
            "AI taxonomy and task types",
            "Data→Model→Prediction pipeline",
            "Evaluation metrics and tradeoffs",
            "Ethics, privacy, fairness, and responsible use"
        ],
        "delivery_examples": [
            "Short micro-lectures with transcripts",
            "Guided Colab notebooks with prewritten cells",
            "Case walkthroughs and think pair share",
            "Debate or fishbowl on policy topics"
        ],
        "context_examples": [
            "Campus services using AI (tutoring chatbots, search ranking)",
            "Sector cases (health, finance, arts, public sector)",
            "Stakeholder memos for non expert audiences"
        ],
        "assessment_examples": [
            "Auto graded quizzes for concepts",
            "Dataset cards and case memos",
            "Lab checkpoints with screenshots and rationale",
            "Final non expert brief and presentation"
        ]
    },
    "accessibility_equity_ethics": [
        "Provide transcripts, alt text, and low bandwidth materials.",
        "Avoid PII in datasets; document consent and provenance.",
        "Offer multiple demonstration modes for the same competency."
    ],
    "notes": "Use this object as shared context for agents to ensure consistent alignment across weekly modules and artifacts."
}


