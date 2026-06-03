---
title: Who Am I Meeting
emoji: 🤝
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.15.1
python_version: "3.10"
app_file: main.py
pinned: false
---

## Live Demo

Hugging Face Space: [Who Am I Meeting](https://huggingface.co/spaces/vishalkajaria/who-am-i-meeting)

## Source Code
GitHub Repository: [Who Am I Meeting Repository](https://github.com/Vishal-kajaria/Who-Am-I-Meeting)




# Who Am I Meeting? 🤝

An AI-powered meeting preparation and meeting history assistant that helps users prepare for interviews, client meetings, networking sessions, sales calls, and partnership discussions by generating company intelligence, meeting talking points, smart questions, preparation checklists, storing meeting history, and exporting downloadable PDF meeting briefs.

Built and deployed using Gradio, OpenAI, LangChain, Serper API, Supabase, and Hugging Face Spaces.

## Features

* Generate company summaries
* Fetch latest company information
* Generate meeting talking points
* Generate smart questions
* Meeting Type support:

  * Job Interview
  * Client Meeting
  * Networking
  * Sales Call
  * Partnership Discussion
* Generate preparation checklists
* Competitor analysis
* Potential challenges and risk analysis
* Key products and services overview
* Company quick facts (Founded Year, Headquarters, Industry, CEO, Website)
* Meeting history storage using Supabase
* View last 10 recent meetings
* PDF export for meeting briefs
* Loading indicator for better user experience

## Tech Stack

* Python
* LangChain
* OpenAI GPT-4.1 Mini
* Serper API
* Supabase
* Gradio
* Git
* GitHub
* Hugging Face Spaces

## Project Structure

```text
main.py          # Main application
README.md        # Project documentation
pyproject.toml   # Project dependencies
uv.lock          # Dependency lock file
.env             # Environment variables (not committed)
```

## Architecture

```text
User Input
↓
Gradio UI
↓
Serper API (Company Research)
↓
LangChain Prompt Construction
↓
OpenAI GPT-4.1 Mini
↓
Meeting Brief Generation
↓
Supabase (Meeting History Storage)
↓
PDF Export
```

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
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
2. User selects a meeting type.
3. Serper API retrieves recent company information.
4. LangChain builds a structured prompt using company data and meeting type.
5. OpenAI generates:

   * Company Summary
   * Company Quick Facts
   * Latest News
   * Key Products & Services
   * Meeting Talking Points
   * Smart Questions
   * Preparation Checklist
   * Competitor Analysis
   * Potential Challenges
6. Results are displayed in a structured meeting brief.
7. User can download the generated meeting brief as a PDF.
8. Meeting details are stored in Supabase for future retrieval.
9. Users can view their recent meeting history.

## Future Improvements

* Meeting Notes & Follow-ups
* Company Logo Integration
* Meeting Dashboard & Analytics
* Search and Filter Meeting History
* Meeting Readiness Score