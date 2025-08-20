import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint  # ✅ latest package
import time
from dotenv import load_dotenv
# Step 1: Set Hugging Face API token

load_dotenv()
# Step 2: Initialize Hugging Face model
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)
# Step 4: Define prompts
prompt1 = PromptTemplate(
    template="You are a helpful assistant that can break down complex user queries into 4-6 subtasks. "
             "Return as a numbered list.\n\nUser query: {topic}\nSubtasks:",
    input_variables=["topic"]
)

# Build chains
parser = StrOutputParser()
chain1 = prompt1 | model | parser   # decomposition

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="AI Task Manager", page_icon="🤖")
st.title("🤖 Robotics Club Task Manager")

# Chat-style input
user_input = st.text_input("Enter your task:", placeholder="e.g., Organize a robotics workshop")


if st.button("Run"):
    if user_input.strip():
        st.chat_message("user").markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown("Breaking into subtasks...")

        # Call model directly
        formatted_prompt = prompt1.format(topic=user_input)
        response = model.invoke(formatted_prompt)   # direct invoke
        subtasks = response.content if hasattr(response, "content") else str(response)

        agen = 1
        for line in subtasks.split("\n"):
            if line.strip():
                with st.chat_message("assistant"):
                    st.markdown(f"⏳ Agent {agen} Working on: {line.strip()}")
                    time.sleep(0.1)
                    st.markdown(f"✅Completed this task!!")
                    agen += 1

