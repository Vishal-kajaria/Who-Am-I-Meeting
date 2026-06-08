from langchain_core.prompts import PromptTemplate
from who_am_I_meeting.llm import llm, parser

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