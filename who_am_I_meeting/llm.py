from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from who_am_I_meeting.config import OPENAI_API_KEY

# Create OpenAI client
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY
)

parser = JsonOutputParser()