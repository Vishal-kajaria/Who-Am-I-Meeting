from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from supabase import create_client
import requests
import os
import gradio as gr

# Load variables from .env file
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

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
    response.raise_for_status()

    # Convert response into Python dictionary
    data = response.json()

    # Store search results
    search_info = ""

    # Loop through first 3 search results
    for result in data.get("organic", [])[:3]:

        title = result["title"]
        snippet = result["snippet"]

        search_info += f"Title: {title}\n"
        search_info += f"Snippet: {snippet}\n\n"
    return search_info  


def generate_meeting_brief(name, company, meeting_type, search_info):
    prompt_template = PromptTemplate.from_template("""
    You are an AI meeting assistant.

    Person Name:
    {name}

    Company:
    {company}

    Meeting Type:
    {meeting_type}

    Latest Company Information:
    {search_info}

    Generate a meeting brief specifically for a {meeting_type}.

    Use the meeting type to tailor:
    - Meeting talking points
    - Smart questions
    - Recommendations

    Generate:

    1. Company Summary
    2. Latest News
    3. Meeting Talking Points
    4. Smart Questions To Ask
    5. Preparation Checklist
    6. Competitor Analysis

    For the company, identify:
    - Major competitors
    - Key differentiators
    - Market position

    7. Potential Challenges

    Identify:
    - Current business challenges
    - Market risks
    - Industry challenges
    - Areas that may require careful discussion
                                                                                                                                        
    8. Key Products & Services

    Identify:
    - Main products
    - Main services
    - Popular offerings
    - Revenue-driving solutions

    9. Company Quick Facts

    Return ONLY in this markdown format:

    - Founded Year: <value>
    - Headquarters: <value>
    - Industry: <value>
    - CEO: <value>
    - Official Website: <value>

    Do not return as a paragraph.
    Do not combine multiple facts on one line.
                                                                        
    Return the response in this JSON format:

    {{
        "company_summary": "",
        "latest_news": "",
        "meeting_talking_points": "",
        "smart_questions": "",
        "preparation_checklist": "",
        "competitor_analysis": "",
        "potential_challenges": "",
        "key_products_services": "",
        "company_quick_facts": ""
    }}                                               
""")    
    chain = prompt_template | llm | parser

    response = chain.invoke(
        {
            "name": name,
            "company": company,
            "meeting_type": meeting_type,
            "search_info": search_info
        }
    )

    return (
        f"## Company Summary\n\n"
        f"{response['company_summary']}\n\n"

        f"## Company Quick Facts\n\n"
        f"{response['company_quick_facts']}\n\n"

        f"## Latest News\n\n"
        f"{response['latest_news']}\n\n"

        f"## Meeting Talking Points\n\n"
        f"{response['meeting_talking_points']}\n\n"

        f"## Smart Questions\n\n"
        f"{response['smart_questions']}\n\n"

        f"## Preparation Checklist\n\n"
        f"{response['preparation_checklist']}\n\n"

        f"## Competitor Analysis\n\n"
        f"{response['competitor_analysis']}\n\n"

        f"## Potential Challenges\n\n"
        f"{response['potential_challenges']}\n\n"

        f"## Key Products & Services\n\n"
        f"{response['key_products_services']}\n\n"
    )


def save_search(person_name, company_name, meeting_type):
    supabase.table("meeting_history").insert(
        {
            "person_name": person_name,
            "company_name": company_name,
            "meeting_type": meeting_type
        }
    ).execute()

def generate_pdf(content, company):

    pdf_file = f"{company.replace(' ', '_')}_meeting_brief.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    story = [
        Paragraph("Meeting Brief", styles["Title"]),
        Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])
    ]

    doc.build(story)

    return pdf_file

def show_loading():
    return "⏳ Generating meeting brief..."

def clear_loading():
    return ""

def who_am_i_meeting(name, company, meeting_type):
    try:
        if not name.strip():
            return "Please enter a person's name."

        if not company.strip():
            return "Please enter a company name."

        if not meeting_type:
            return "Please select a meeting type."

        search_info = search_company(company)

        meeting_brief = generate_meeting_brief(
            name,
            company,
            meeting_type,
            search_info
        )

        save_search(name,company,meeting_type)

        pdf_file = generate_pdf(meeting_brief, company)
        
        return meeting_brief, pdf_file
    except Exception as e:
        return f"An error occurred: {str(e)}", None

with gr.Blocks() as app:

    gr.Markdown("# Who Am I Meeting? 🤝")

    gr.Markdown("""
    Generate an AI-powered meeting brief using live company information.
    """)

    with gr.Row():

        with gr.Column(scale=1):

            name_input = gr.Textbox(
                label="Person Name",
                placeholder="Enter the person's name"
            )

            company_input = gr.Textbox(
                label="Company Name",
                placeholder="Enter the company name"
            )
            meeting_type = gr.Dropdown(
                choices=[
                    "Job Interview",
                    "Client Meeting",
                    "Networking",
                    "Sales Call",
                    "Partnership Discussion"
                ],
                label="Meeting Type"
            )
            generate_button = gr.Button("Generate Brief")

        with gr.Column(scale=2):
            status_box = gr.Markdown()
            output_box = gr.Markdown(height=600)
            pdf_output = gr.File(label="Download Meeting Brief")

    generate_button.click(
        fn=show_loading,
        outputs=status_box
    ).then(
        fn=who_am_i_meeting,
        inputs=[name_input, company_input, meeting_type],
        outputs=[output_box, pdf_output]
    ).then(
        fn=clear_loading,
        outputs=status_box
    )

if __name__ == "__main__":
    app.launch()