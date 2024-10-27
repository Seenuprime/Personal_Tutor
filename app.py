from flask import Flask, render_template, request
from forms import Query
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the environment variable and LLM
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model='gemma2-9b-it')

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
        give some greetings at the end. 
    """
    prompt_template = PromptTemplate(
        input_variables=['topic'],
        template=template
    )
    return prompt_template.format(topic=topic)

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dab152770d8586850fa88528c67b9a78'

@app.route('/', methods=['GET', 'POST'])
def home():
    query = Query()
    result = None  # Default result

    # Check if the form is submitted
    if request.method == 'POST' and query.validate_on_submit():
        # Retrieve the query from the form
        user_topic = query.query.data
        # Generate prompt and invoke LLM
        prompt_text = prompt(user_topic)
        result = llm.invoke(prompt_text).content

    return render_template("index.html", query=query, result=result)

if __name__ == "__main__":
    app.run(debug=True)
