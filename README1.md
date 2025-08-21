 🤖 Agentic Chatbot Demo

This project is a **mock agentic chatbot demo** that takes a single user query (e.g.,  
_"Organize a robotics workshop"_) and automatically **breaks it down into subtasks** such as:

- Book venue  
- Email coordinator  
- Prepare poster  

Each subtask is then "handled" by a **mock agent** (no real external APIs), and the chatbot displays a **progress log** of how the query is executed step by step.  

✨ This project is for demonstration purposes only — it mimics the flow of agentic task execution, but does not actually send emails or book venues.

---

## 🚀 Features
- Accepts a **high-level task** from the user.
- Dynamically **splits task into subtasks** using an LLM.  
- Assigns subtasks to **mock agents** (simulated).  
- Displays **progress logs** of execution in chat format.  
- Simple, lightweight, and easy to extend.  

---

## 🛠️ Tech Stack
- **Python 3.9+**  
- **LangChain** for LLM orchestration  
- **Groq / Gemini / OpenAI** (choose one provider as backend)  
- **Streamlit / CLI / Vercel** for UI (depending on setup)


here is the link: https://e9pf2ndbuue4utrkbgh87u.streamlit.app/
