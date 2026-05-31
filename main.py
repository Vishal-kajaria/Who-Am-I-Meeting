from langchain_openai import ChatOpenAI
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
    """)

    prompt = prompt_template.format(
        name=name,
        company=company,
        search_info=search_info
    )

    response = llm.invoke(prompt)

    return response.content

def who_am_i_meeting(name, company):

    search_info = search_company(company)

    meeting_brief = generate_meeting_brief(
        name,
        company,
        search_info
    )

    return meeting_brief

app = gr.Interface(
    fn=who_am_i_meeting,
    inputs=["text", "text"],
    outputs="text",
    title="Who Am I Meeting?",
    description="AI Meeting Assistant"
)


if __name__ == "__main__":
    app.launch()