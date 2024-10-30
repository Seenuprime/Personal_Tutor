from flask import Flask, render_template, request
from forms import Query, Topic_Query
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




def topic_prompt(topic):
    template = """
        Please provide an in-depth explanation of the topic '{topic}',.
        Add some new lines to make it look cool use html use lower head tags from h3-h6 with 2 new lines for each topic.
        Use pre tag only to show the code.
        Covering its significance, core concepts, practical applications, challenges, and future trends and provide code if necessary. 
        Offer clear and comprehensive information, structured to give a well-rounded understanding of the topic.
        Give some sorces for each tipics to refer with direct like in 'a' tag.
        should be in this format:
        <h3><b>main topic</b></h3><br>
            <h2>sub topic</h2>
                <b>(content name):</b>
                <p>content</p>
                <b>(content name):</b>
                <p>content</p>
                <pre> code (if necessary)</pre>
                <a> link (reference) </a> (open on new tab)
                <br>
            <h2>sub topic</h2>
                <b>(content name):</b>
                <p>content</p>
                <b>(content name):</b>
                <p>content</p>
                <pre> code (if necessary)</pre>
                <a> link to resources</a> (open on new tab)
                <br>
        
    """
    prompt_template = PromptTemplate(
        input_variables=['topic'],
        template=template
    )
    return prompt_template.format(topic=topic)

topic_llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview")

@app.route('/topics', methods=['GET', 'POST'])
def topics():
    topic_query = Topic_Query()
    topic_result = None

    if request.method == 'POST' and topic_query.validate_on_submit():
        topic_user_topic = topic_query.query.data
        topic_prompt_text = topic_prompt(topic_user_topic)
        topic_result = topic_llm.invoke(topic_prompt_text).content
    return render_template('topics.html', topic_query=topic_query, topic_result=topic_result)


if __name__ == "__main__":
    app.run(debug=True)
