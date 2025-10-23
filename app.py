import gradio as gr
from crew import HaileiCrew

# ------------------------------------------
# Initialize HAILEI Crew (Coordinator only)
# ------------------------------------------
hailei_crew = HaileiCrew()
crew = hailei_crew.crew()

# ------------------------------------------
# Global session course storage
# ------------------------------------------
session_course_request = {}


# ------------------------------------------
# Step 1: Form submission → Coordinator kickoff
# ------------------------------------------
def run_coordinator_agent(course_title, description, credits, duration_weeks, level, expectations):
    """Validate input and start Coordinator Agent conversation."""
    errors = []

    # --- Validation Rules ---
    if not course_title or len(course_title.strip()) < 5:
        errors.append("⚠️ Course title must be at least 5 characters long.")
    if not description or len(description.strip()) < 15:
        errors.append("⚠️ Course description must be at least 15 characters long.")
    if not expectations or len(expectations.strip()) < 10:
        errors.append("⚠️ Course expectations must be at least 10 characters long.")
    if not isinstance(credits, (int, float)) or credits <= 0:
        errors.append("⚠️ Please enter a valid number of credits.")
    if not isinstance(duration_weeks, (int, float)) or duration_weeks <= 0:
        errors.append("⚠️ Duration (weeks) must be greater than 0.")

    # --- If validation fails ---
    if errors:
        return "\n".join(errors), None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

    # --- Store input globally ---
    global session_course_request
    session_course_request = {
        "course_title": course_title.strip(),
        "course_description": description.strip(),
        "course_credits": int(credits),
        "course_duration_weeks": int(duration_weeks),
        "course_level": level,
        "course_expectations": expectations.strip(),
        "course_modules": []
    }
    print("[DEBUG] Session course request: ", session_course_request)
    # --- Run the Coordinator ---
    result = crew.kickoff(inputs={"course_request": session_course_request})
    print(result)
    reply = getattr(result, "raw_output", str(result))

    # --- Fallback if LLM returns empty ---
    if not reply or reply.strip() == "":
        reply = (
            f"🧠 Thank you for submitting your course **{course_title.strip()}**!\n\n"
            "Let’s go over a few details to make sure I understand your course intent correctly."
        )

    history = [("assistant", reply)]

    # Hide form, show chat
    return (
        "",  # clear message
        history,  # chat history
        gr.update(visible=True),  # show chatbot
        gr.update(visible=True),  # show user input
        gr.update(visible=True),  # show send_btn
        gr.update(visible=False), # hide form
    )


# ------------------------------------------
# Step 2: Ongoing conversation with Coordinator
# ------------------------------------------
def coordinator_chat(message, history):
    """Continue Coordinator conversation after form submission."""
    global session_course_request

    if not session_course_request:
        history.append(("assistant", "⚠️ Please submit the course form first."))
        return "", history

    # Approve → end of Coordinator phase
    if message.strip().lower() == "approve":
        history.append(("user", message))
        history.append(("assistant", "✅ Approved! I’ll now prepare to delegate this to IPDAi for instructional design."))
        return "", history

    # Otherwise, normal dialogue
    response = crew.kickoff(inputs={"course_request": {**session_course_request, "user_message": message}})
    reply = getattr(response, "raw_output", str(response))

    history.append(("user", message))
    history.append(("assistant", reply))
    return "", history


# ------------------------------------------
# Build Gradio UI
# ------------------------------------------
with gr.Blocks(title="🎓 HAILEI 3.0 - Coordinator Agent") as demo:
    gr.Markdown("""
    # 🧠 HAILEI4T Coordinator Agent  
    The Coordinator Agent will guide you through refining your course request before design begins.  
    Fill out the form below, submit, and then chat interactively.  
    Type **"approve"** once you’re satisfied.
    """)

    # ---------- FORM PHASE ----------
    with gr.Group(visible=True) as form_section:
        gr.Markdown("### 📋 Course Request Form")

        with gr.Row():
            course_title = gr.Textbox(label="Course Title", placeholder="Introduction to Artificial Intelligence")
            course_description = gr.Textbox(label="Course Description", lines=3)

        with gr.Row():
            course_credits = gr.Number(label="Credits", value=3)
            course_duration_weeks = gr.Number(label="Duration (weeks)", value=16)

        with gr.Row():
            course_level = gr.Dropdown(
                label="Course Level",
                choices=[
                    "Undergraduate - Introductory",
                    "Undergraduate - Advanced",
                    "Graduate - Introductory",
                    "Graduate - Advanced",
                    "Professional Certificate",
                ],
                value="Undergraduate - Introductory"
            )
            course_expectations = gr.Textbox(label="Course Expectations", lines=2)

        submit_btn = gr.Button("🚀 Submit to Coordinator")
        validation_msg = gr.Markdown()

    # ---------- CHAT PHASE ----------
    gr.Markdown("### 💬 Coordinator Chat Mode")

    chatbot = gr.Chatbot(
        label="🧩 Coordinator Conversation",
        height=450,
        bubble_full_width=False,
        show_copy_button=True,
        visible=False
    )

    user_input = gr.Textbox(
        placeholder="Ask or clarify details with the Coordinator...",
        show_label=False,
        visible=False
    )

    send_btn = gr.Button("💬 Send Message", visible=False)

    send_btn.click(
        coordinator_chat,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot],
    )

    # Form submission → validation + chat kickoff
    submit_btn.click(
        run_coordinator_agent,
        inputs=[
            course_title,
            course_description,
            course_credits,
            course_duration_weeks,
            course_level,
            course_expectations,
        ],
        outputs=[
            validation_msg,
            chatbot,
            chatbot,
            user_input,
            send_btn,
            form_section,  # hide form after valid submit
        ],
    )

demo.launch()
