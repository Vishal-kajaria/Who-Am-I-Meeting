from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import requests
import os
import gradio as gr

# Load variables from .env file
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


# Create OpenAI client
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY
)

parser = JsonOutputParser()

def search_company(company):
    # Serper API URL
    url = "https://google.serper.dev/search"

    # Search query
    payload = {
        "q": company
    }

    # API headers
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    # Send request to Serper
    response = requests.post(url, json=payload, headers=headers)

    # Convert response into Python dictionary
    data = response.json()

    # Store search results
    search_info = ""

    # Loop through first 3 search results
    for result in data["organic"][:3]:

        title = result["title"]
        snippet = result["snippet"]

        search_info += f"Title: {title}\n"
        search_info += f"Snippet: {snippet}\n\n"
    return search_info  


def generate_meeting_brief(name, company, search_info):
    prompt_template = PromptTemplate.from_template("""
    You are an AI meeting assistant.

    Person Name:
    {name}

    Company:
    {company}

    Latest Company Information:
    {search_info}

    Generate:
    1. Company Summary
    2. Latest News
    3. Meeting Talking Points
    4. Smart Questions To Ask
    
    Return the response in this JSON format:

    {{
        "company_summary": "",
        "latest_news": "",
        "meeting_talking_points": "",
        "smart_questions": ""
    }}
                                                   
""")
    
    chain = prompt_template | llm | parser

    response = chain.invoke(
        {
            "name": name,
            "company": company,
            "search_info": search_info
        }
    )

    return f"""
    Company Summary:
    {response['company_summary']}

    Latest News:
    {response['latest_news']}

    Meeting Talking Points:
    {response['meeting_talking_points']}

    Smart Questions:
    {response['smart_questions']}
    """

def who_am_i_meeting(name, company):

    if not name.strip():
        return "Please enter a person's name."

    if not company.strip():
        return "Please enter a company name."

    search_info = search_company(company)

    meeting_brief = generate_meeting_brief(
        name,
        company,
        search_info
    )

    return meeting_brief

app = gr.Interface(
    fn=who_am_i_meeting,
    inputs=[
        gr.Textbox(
            label="Person Name",
            placeholder="Enter the person's name"
        ),
        gr.Textbox(
            label="Company Name",
            placeholder="Enter the company name"
        )
    ],
    outputs=gr.Textbox(
        label="Meeting Brief",
        lines=20
    ),

    title="Who Am I Meeting? 🤝",
    description="""
    Generate an AI-powered meeting brief using live company information.

    Enter a person's name and company name to receive:
    • Company Summary
    • Latest News
    • Meeting Talking Points
    • Smart Questions To Ask
    """,

    submit_btn="Generate Brief",
    clear_btn="Reset"
)


if __name__ == "__main__":
    app.launch()