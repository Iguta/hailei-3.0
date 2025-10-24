import gradio as gr
import os
from dotenv import load_dotenv
from crew import HaileiCrew

from models.course_request import CourseRequest
from models.cordinator_state import CoordinatorState

coordinator_state = CoordinatorState()

# Load environment variables from .env file
load_dotenv()

# ------------------------------------------
# Initialize HAILEI Crew (Coordinator only)
# ------------------------------------------
hailei_crew = HaileiCrew()
crew = hailei_crew.crew()

# ------------------------------------------
# Global session course storage
# ------------------------------------------
coordinator_state = CoordinatorState()  # initialize the coordinator state


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


    global coordinator_state

    try:
        request = CourseRequest(
            course_title=course_title,
            course_description=description,
            course_credits=int(credits),
            course_duration_weeks=int(duration_weeks),
            course_level=level,
            course_expectations=expectations,
        )
    except Exception as e:
        return f"⚠️ Validation Error: {str(e)}", None, gr.update(visible=True)


    coordinator_state.reset()
    coordinator_state.course_request = request

    response = crew.kickoff(inputs=coordinator_state.dict())

    reply = getattr(response, "raw_output", str(response))
    coordinator_state.add_assistant_message(reply)

    history = [("assistant", reply)]

    return "", history, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)


# ------------------------------------------
# Step 2: Ongoing conversation with Coordinator
# ------------------------------------------
def coordinator_chat(message, history):
    """Continue Coordinator conversation after form submission."""
    global coordinator_state

    if not coordinator_state.course_request:
        history.append(("assistant", "⚠️ Please submit the course form first."))
        return "", history

    # Approve → end of Coordinator phase
    if message.strip().lower() == "approve":
        history.append(("user", message))
        history.append(("assistant", "✅ Approved! I'll now prepare to delegate this to IPDAi for instructional design."))
        return "", history

    # Add user message to conversation history
    coordinator_state.add_user_message(message)
    
    # Continue the conversation with context
    response = crew.kickoff(inputs=coordinator_state.dict())
    reply = getattr(response, "raw_output", str(response))

    # Add assistant response to conversation history
    coordinator_state.add_assistant_message(reply)
    
    # Update Gradio history
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

    send_btn = gr.Button("Send Message", visible=False)

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
