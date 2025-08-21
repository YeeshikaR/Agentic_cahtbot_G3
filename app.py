import streamlit as st
from utils import break_into_subtasks, subtask
import time

st.set_page_config(page_title="Agentic Chatbot Demo", layout="centered")

st.title("Agentic Chatbot demo")
st.write("Enter a query to get chat bot")

query = st.text_input("Enter your query:", placeholder="e.g., Organize a workshop")

if st.button("Get Subtasks"):
    if query:
        subtasks = break_into_subtasks(query)
        st.write(f"### Main Task: {query}")
        
        for i, task in enumerate(subtasks, start=1):
            st.markdown(f"*Subtask {i}: {task}*")
            logs = subtask(task)
            for log in logs:
                st.info(log)
                time.sleep(0.7)  # mimic progress
    else:
        st.warning("Please enter task")








# import streamlit as st

# def breakdown_task(task):
#     # Basic logic to split user task into subtasks
#     words = task.lower().split()
#     if "workshop" in words:
#         return ["Define topic & agenda", "Book venue", "Email coordinator", "Design and print poster"]
#     else:
#         return ["Analyze", "Plan", "Execute", "Review"]

# if "logs" not in st.session_state:
#     st.session_state.logs = []

# st.title("Agentic Chatbot Demo")
# prompt = st.chat_input("Enter your task, e.g., 'Organize a robotics workshop'")

# if prompt:
#     st.session_state.logs.append(("user", prompt))

#     subtasks = breakdown_task(prompt)

#     for sub in subtasks:
#         st.session_state.logs.append(("assistant", f"🕵️ Sub-task: {sub}"))
#         st.session_state.logs.append(("assistant", f"[{sub}] – In progress..."))
#         st.session_state.logs.append(("assistant", f"[{sub}] – Done!"))

#     st.session_state.logs.append(("assistant", "All subtasks completed!"))

# # Render chat
# for role, message in st.session_state.logs:
#     with st.chat_message(role):
#         st.write(message)
