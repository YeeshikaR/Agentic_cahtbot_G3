from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st
import os

load_dotenv()

model1 = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0)
st.title("Steps to perform a task")

agents = ['Agent1', 'Agent2', 'Agent3', 'Agent4', 'Agent5'] #list of agents

prompt1 = PromptTemplate(
    template="""Task: {task}
    Return the result as a valid JSON array of exactly 5 strings.
    Do not include any explanations or text, only the JSON array.
    Example output:
    ["step1", "step2", "step3", "step4", "step5"].""",
    input_variables=['task']
)

task = st.text_input('Enter task : ')

parser1 = JsonOutputParser()

chain1 = prompt1 | model1 | parser1
if st.button('Get Steps'):

    result1 = chain1.invoke({
        'task' : task
    })

    print(type(result1))

    st.header("List of Subtasks : \n")
    
    for task in result1:  
        st.write("->",task)

    agent_subtask={}   # dictionary to hold agent and their assigned subtask
    i = 0
    for agent in agents:
        agent_subtask[agent] = result1[i]
        i += 1

    def return_status(agent_name, subtask):      # a function mocking a progress log of an agent
        st.divider()
        st.write(f"**Subtask:** {subtask}  ::  **Agent:** {agent_name}")
        st.write("Status: Initializing task")
        st.write("Status: In progress")
        st.write("Status: Completed successfully")

    st.header("Status of each subtask : \n")

    for agent in agent_subtask.keys():  # iterate through each agent and their assigned subtask 
        return_status(agent, agent_subtask[agent])