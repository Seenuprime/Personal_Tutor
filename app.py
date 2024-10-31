import os
import re
import io
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, session
from fpdf import FPDF
from forms import Query, Topic_Query
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize the LLMs
llm = ChatGroq(model='gemma2-9b-it')
topic_llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview")

# Define prompt functions
def prompt(topic):
    template = """
        You are an assistant that helps organize learning paths by identifying key topics and their subtopics for the topic "{topic}". 
        The user wants to learn about {topic}. 
        Please provide a structured list of the main topics and relevant subtopics that the user should explore to gain a comprehensive understanding of {topic}. 

        Organize the topics in a hierarchical format (with no whitespaces):

        <h5>Here's a structured learning path for {topic}, broken down into key topics and subtopics:</h5>

        <ol>
            <li>
                <strong>Topic 1</strong>
                <ul>
                    <li>Subtopic 1.1</li>
                    <li>Subtopic 1.2</li>
                </ul>
            </li>
            <li>
                <strong>Topic 2</strong>
                <ul>
                    <li>Subtopic 2.1</li>
                    <li>Subtopic 2.2</li>
                </ul>
            </li>
        </ol>

        Keep the structure clear, concise, and easy to follow.
        Give some greetings at the end. 
    """
    prompt_template = PromptTemplate(
        input_variables=['topic'],
        template=template
    )
    return prompt_template.format(topic=topic)

def topics_prompt(topic):
    template = """
        Please provide a detailed explanation of the topic '{topic}'.
        Use HTML formatting with <h3> to <h6> tags to structure sections, adding two new lines after each main section for readability.
        Wrap code examples in <pre> tags.
        
        Structure as follows:
        <h3><b>Main Topic</b></h3><br>
        <h4>Subtopic 1</h4>
            <b>(Section Title):</b>
            <p>Content goes here...</p>
            <pre> Code example here (if necessary) </pre>
            <a href="https://example.com" target="_blank">Reference Link(actual name)</a><br>
            
        <h4>Subtopic 2</h4>
            <b>(Section Title):</b>
            <p>Content goes here...</p>
            <pre> Code example here (if necessary) </pre>
            <a href="https://example.com" target="_blank">Reference Link(actual name)</a><br>

        Each subtopic should have a broad answer with a clear explanation of its significance, core concepts, practical applications, challenges, and future trends, with code samples where relevant.
    """
    
    prompt_template = PromptTemplate(
        input_variables=['topic'],
        template=template
    )
    return prompt_template.format(topic=topic)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key =  'dab152770d8586850fa88528c67b9a78'  

@app.route('/', methods=['GET', 'POST'])
def home():
    query = Query()
    result = None  # Default result

    # Check if the form is submitted
    if request.method == 'POST' and query.validate_on_submit():
        user_topic = query.query.data  # Retrieve the query from the form
        prompt_text = prompt(user_topic)  # Generate prompt and invoke LLM
        try:
            response = llm.invoke(prompt_text)
            result = response.content if response else "No content generated. Please try again."
            
        except Exception as e:
            result = f"Error generating content: {e}"

    return render_template("index.html", query=query, result=result)

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    topic_query = Topic_Query()
    topic_result = None

    if request.method == 'POST' and topic_query.validate_on_submit():
        topic_user_topic = topic_query.query.data
        topic_prompt_text = topics_prompt(topic_user_topic)
        try:
            response = topic_llm.invoke(topic_prompt_text)
            topic_result = response.content if response else "No content generated. Please try again."
        except Exception as e:
            topic_result = f"Error generating content: {e}"

    return render_template('topics.html', topic_query=topic_query, topic_result=topic_result)


if __name__ == "__main__":
    app.run(debug=True)
