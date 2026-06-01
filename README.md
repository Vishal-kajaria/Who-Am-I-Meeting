# Who Am I Meeting? 🤝

An AI-powered meeting preparation assistant built with LangChain, OpenAI, Serper, and Gradio.

## Features

* Generate company summaries
* Fetch latest company information
* Create meeting talking points
* Generate smart questions to ask during meetings
* Loading indicator for better user experience

## Tech Stack

* Python
* LangChain
* OpenAI GPT-4.1 Mini
* Serper API
* Gradio

## Project Structure

```text
main.py          # Main application
README.md        # Project documentation
pyproject.toml   # Project dependencies
uv.lock          # Dependency lock file
.env             # Environment variables (not committed)
```

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Installation

Install dependencies:

```bash
uv sync
```

## Run the Application

```bash
uv run python main.py
```

The application will start locally at:

```text
http://127.0.0.1:7860
```

## How It Works

1. User enters a person's name and company name.
2. Serper API retrieves recent company information.
3. LangChain creates a prompt using the company data.
4. OpenAI generates:

   * Company Summary
   * Latest News
   * Meeting Talking Points
   * Smart Questions
5. Results are displayed in a user-friendly interface.

## Future Improvements

* Deployment on Hugging Face Spaces
* Better UI styling and themes
* Company logo integration
* Export results to PDF
* Meeting history storage
