PRRR_FRAMEWORK = {
    "summary": "PRRR ensures each experience is Personal, Relatable, Relative, and Real to drive inclusion, engagement, and ethical relevance.",
    "how_to_use": "Every activity should touch at least two PRRR dimensions. Make relevance explicit in prompts, rubrics, and feedback.",
    "dimensions": {
        "personal": "Elicit prior experiences, goals, and choice of dataset/topic.",
        "relatable": "Use analogies and cross disciplinary links that honor diverse perspectives.",
        "relative": "Compare options, methods, metrics, risks, and benefits.",
        "real_world": "Anchor tasks in authentic stakeholders, decisions, and constraints."
    },
    "infusion_prompts": [
        "Personal Describe an AI tool you used recently. What did it help with and where did it fall short",
        "Relatable Explain training vs inference using a familiar analogy such as studying vs taking an exam",
        "Relative For your scenario which error is worse false positive or false negative and why",
        "Real world Draft an email advising a non expert on adopting an AI tool with benefits risks and mitigations",
        "Relatable Compare classification to sorting mail and regression to estimating delivery time",
        "Relative Choose two models and justify a recommendation using stakeholder aligned metrics"
    ],
    "ai_course_defaults": {
        "personalization_levers": [
            "Student selected open datasets aligned to major",
            "Choice of use case domain per module",
            "Reflection on value tradeoffs and comfort with risk"
        ],
        "relatability_patterns": [
            "Everyday analogies for core concepts",
            "Examples from multiple cultures and sectors",
            "Visuals and stories before formalism"
        ],
        "relative_frameworks": [
            "Confusion matrix plus cost framing",
            "Model comparison tables with metrics and tradeoffs",
            "Human rules vs data driven approaches"
        ],
        "real_world_outputs": [
            "Dataset cards and risk registers",
            "Stakeholder briefs and one pagers",
            "Policy snippets and responsible use guidelines"
        ]
    },
    "ethics_guardrails": [
        "Disclose limitations and uncertainty.",
        "Avoid sensitive data; document assumptions and mitigations.",
        "Encourage respectful debate and multiple viewpoints."
    ],
    "notes": "Use this object to embed PRRR signals in prompts, examples, rubrics, and peer review so relevance stays visible and accountable."
}