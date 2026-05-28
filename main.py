from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Take user input
name = input("Enter person name: ")
company = input("Enter company name: ")

# Prompt for AI
prompt = f"""
Generate a professional meeting brief for meeting {name} from {company}.

Include:
1. Company summary
2. Possible discussion topics
3. Smart questions to ask
4. Potential risks
"""

# Send request to OpenAI
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Print result
print("\n===== MEETING BRIEF =====\n")
print(response.choices[0].message.content)