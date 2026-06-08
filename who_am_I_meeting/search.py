import requests
from who_am_I_meeting.config import SERPER_API_KEY

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
    response = requests.post(url, json=payload, headers=headers, timeout=15)
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