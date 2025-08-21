import time
import streamlit as st

st.set_page_config(page_title="Agentic Task Planner", page_icon="🤖")
st.title("Agentic Task Planner — Demo")

query = st.text_input("What do you want to do?", "Organize a robotics workshop")

def generate_subtasks(query: str):
    subtasks = []
    text = query.lower()
    if "workshop" in text or "event" in text:
        subtasks = ["Define objectives", "Book venue", "Invite speakers", 
                    "Arrange equipment", "Promote the event", "Prepare agenda", "Conduct workshop", "Collect feedback"]
    elif "website" in text:
        subtasks = ["Define purpose", "Design wireframe", "Develop frontend", 
                    "Set up backend", "Test website", "Deploy online", "Promote launch"]
    elif "project" in text or "app" in text:
        subtasks = ["Brainstorm features", "Set up repository", 
                    "Develop core modules", "Test functionality", "Prepare documentation", "Deploy final version"]
    else:
        subtasks = ["Research task", "Break into steps", "Assign responsibilities", "Execute plan", "Review & improve"]

    return subtasks

if st.button("Generate Plan"):
    tasks = generate_subtasks(query)
    st.subheader(f"Plan for: {query}")

    for i, task in enumerate(tasks, start=1):
        with st.chat_message("assistant"):
            st.write(f"Agent {i} working on: {task}")
        time.sleep(0.4)
        with st.chat_message("assistant"):
            st.write(f"Agent {i} completed: {task} ✅")

    st.success("All agents finished their tasks!")
