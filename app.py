import gradio as gr
import os
import json, re
from dotenv import load_dotenv
from crew import HaileiCrew
from models.models import CoordinatorState, CourseRequest

# ------------------------------------------
# Setup
# ------------------------------------------
load_dotenv()
hailei_crew = HaileiCrew()
coordinator_state = CoordinatorState()

# ------------------------------------------
# Step 1: Form submission → Coordinator kickoff
# ------------------------------------------
def run_coordinator_agent(course_title, description, credits, duration_weeks, level, expectations):
    """Validate input and start Coordinator Agent conversation."""
    errors = []

    # --- Validation ---
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

    if errors:
        return (
            "\n".join(errors),
            None,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
        )

    # --- Build CourseRequest ---
    course_request_data = {
        "course_title": course_title.strip(),
        "course_description": description.strip(),
        "course_credits": int(credits),
        "course_duration_weeks": int(duration_weeks),
        "course_level": level,
        "course_expectations": expectations.strip(),
    }

    coordinator_state.reset()
    coordinator_state.course_request = CourseRequest(**course_request_data)
    print("[DEBUG] Initial course_request:", coordinator_state.course_request.dict())

    # --- Kick off Coordinator ---
    response = hailei_crew.kickoff_coordination(coordinator_state)
    raw_reply = getattr(response, "raw_output", str(response))

    # --- Extract JSON updates (if any) ---
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_reply, re.DOTALL)
    if json_match:
        try:
            updates = json.loads(json_match.group(1))
            coordinator_state.course_request = coordinator_state.course_request.copy(update=updates)
            print("[DEBUG] Updated CourseRequest:", coordinator_state.course_request.dict())
            display_reply = raw_reply.replace(json_match.group(0), "").strip()
        except Exception as e:
            print("[WARN] Could not parse JSON:", e)
            display_reply = raw_reply
    else:
        display_reply = raw_reply

    # --- Initialize chat history ---
    coordinator_state.add_assistant_message(display_reply)
    history = [("assistant", display_reply)]

    # Hide form, show chat + approve button
    return (
        "",
        history,
        gr.update(visible=True),   # show chatbot
        gr.update(visible=True),   # show user_input
        gr.update(visible=True),   # show send_btn
        gr.update(visible=False),  # hide form
        gr.update(visible=True),   # show approve button
    )

# ------------------------------------------
# Step 2: Continue conversation
# ------------------------------------------
def coordinator_chat(message, history):
    """Continue Coordinator conversation after form submission."""
    global coordinator_state

    if not coordinator_state.course_request:
        history.append(("assistant", "⚠️ Please submit the form first."))
        return "", history

    coordinator_state.add_user_message(message)
    response = hailei_crew.kickoff_coordination(coordinator_state)
    raw_reply = getattr(response, "raw_output", str(response))

    # --- Split Markdown vs JSON ---
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_reply, re.DOTALL)
    if json_match:
        try:
            updates = json.loads(json_match.group(1))
            coordinator_state.course_request = coordinator_state.course_request.copy(update=updates)
            print("[DEBUG] Updated course_request:", coordinator_state.course_request.dict())
            display_reply = raw_reply.replace(json_match.group(0), "").strip()
        except Exception as e:
            print("[WARN] Could not parse JSON:", e)
            display_reply = raw_reply
    else:
        display_reply = raw_reply

    coordinator_state.add_assistant_message(display_reply)
    history.append(("user", message))
    history.append(("assistant", display_reply))
    return "", history

# ------------------------------------------
# Step 3: Approve button → trigger IPDAi
# ------------------------------------------
def approve_course_design(history):
    """Triggered when user clicks Approve button."""
    history.append(("assistant", "✅ Approved! Delegating your finalized course request to IPDAi for instructional design..."))

    coordinator_state.approved = True
    design_response = hailei_crew.kickoff_design_phase(coordinator_state)
    design_reply = getattr(design_response, "raw_output", str(design_response))

    coordinator_state.add_assistant_message(design_reply)
    history.append(("assistant", design_reply))
    return history

# ------------------------------------------
# Build Gradio UI
# ------------------------------------------
with gr.Blocks(title="🎓 HAILEI 3.0 - Coordinator Agent") as demo:
    gr.Markdown("""
    # 🧠 HAILEI4T Coordinator Agent  
    The Coordinator Agent will guide you through refining your course request before design begins.  
    Fill out the form below, submit, and then chat interactively.  
    Once you’re satisfied, click **✅ Approve & Generate Course Design** to proceed to IPDAi.
    """)

    # ---------- FORM ----------
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

    # ---------- CHAT ----------
    gr.Markdown("### 💬 Coordinator Chat Mode")
    chatbot = gr.Chatbot(label="🧩 Coordinator Conversation", height=450, visible=False)
    user_input = gr.Textbox(placeholder="Ask or clarify details...", show_label=False, visible=False)
    send_btn = gr.Button("💬 Send Message", visible=False)
    approve_btn = gr.Button("✅ Approve & Generate Course Design", visible=False)

    # ---------- Interactions ----------
    send_btn.click(coordinator_chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

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
            form_section,
            approve_btn,
        ],
    )

    approve_btn.click(approve_course_design, inputs=[chatbot], outputs=[chatbot])

demo.launch()
