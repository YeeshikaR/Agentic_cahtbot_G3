Live link: https://yee-task2-khccmqswot3cbscbjm4buj.streamlit.app/

###Overview<br>
This project demonstrates a dynamic agentic task management system using a chatbot interface. A user can input a high-level task, and the system automatically breaks it down into five subtasks. Each subtask is assigned to a mock agent (Agent1, Agent2, …), and a progress log is displayed, simulating real-time task completion.<br>

###Approach<br>
->Task Input:<br>
    Users provide a high-level task via a Streamlit text input box.<br>
->Subtask Generation:<br>
    The input task is sent to Google Generative AI (Gemini 1.5) via LangChain. A prompt instructs the AI to return exactly five subtasks as a JSON array.<br>
->Agent Assignment:<br>
    Each generated subtask is assigned to a pre-defined mock agent (Agent1–Agent5).<br>
->Dynamic Progress Logs:<br>
    For each agent-subtask pair, a progress log is dynamically displayed in Streamlit:<br>
      Initializing task<br>
      In progress<br>
      Completed successfully<br>
->Interactive Display:<br>
    Subtasks are displayed as a list.<br>
    Each agent’s progress log is displayed sequentially, simulating task execution.<br>
