from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)


st.header('Research Tool')


# user_input=st.text_input('Enter your prompt')

# paper_input=st.selectbox("Select Reasearch Paper Name",["Select...","who is prime minister of india","option 2","option 3"])
# style_input=st.selectbox("Select explation style",["Beginner-friendly","Technical","code-oriented"])
# length_input=st.selectbox("Select length of explaination",["Short","medium","long"])


# # templet
# templet=PromptTemplate(
#     template="""
#     please summarise rearch paper titled "{paper_input}" with the following specifications:
#     Explation Style:{style_input}
#     explation length:{length_input}
# """,
# input_variables=["paper_input","style_input","length_input"]
# )





# from langchain.prompts import PromptTemplate
user_query=st.text_input('Enter your prompt')
template = PromptTemplate(
    template="""
    You are an AI task planner. Break the following user query into subtasks 
    and assign each subtask to a mock agent. For each agent, simulate progress logs.

    User Query: "{user_query}"

    Expected Output Format:
    - Subtasks list (step by step)
    - For each subtask:
        • Agent assigned
        • Progress logs (at least 3 steps)
        • Final status (Completed ✅)

    Generate a dynamic plan that fits the given query.
    """,
    input_variables=["user_query"]
)


##########without chaining
# prompt=templet.invoke({
#     'paper_input':paper_input,
#     'style_input':style_input,
#     'length_input':length_input
# })
# if st.button("submit"):
#     result=model.invoke(prompt)
#     st.write(result.content)

########### chaining

if st.button("submit"):
    chain=template | model
    result=chain.invoke({
        'user_query':user_query
        # 'paper_input':paper_input,
        # 'style_input':style_input,
        # 'length_input':length_input
    })


    # prompt=templet.invoke()
    # result=model.invoke(prompt)
    st.write(result.content)


    