import streamlit as st 
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

st.title("🎓 Welcome To Personal Tutor! 📚")

topic = st.text_input("What Topic you want to learn:")

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model='gemma2-9b-it')

def prompt(topic):
    template = """
        You are an assistant that helps organize learning paths by identifying key topics and their subtopics for the topic "{topic}". 
        The user wants to learn about {topic}. 
        Please provide a structured list of the main topics and relevant subtopics that the user should explore to gain a comprehensive understanding of {topic}. 

        Organize the topics in a hierarchical format:

        1. Topic 1 /n
        - Subtopic 1.1 /n
        - Subtopic 1.2 /n/n
        2. Topic 2 /n
        - Subtopic 2.1 /n
        - Subtopic 2.2 /n

        Keep the structure clear, concise, and easy to follow.
    """
    prompt_template = PromptTemplate(
        input_variables = ['topic'],
        template=template
    )
    return prompt_template.format(topic=topic)



if topic:
    result = llm.invoke(prompt(topic))

    st.write(result.content)