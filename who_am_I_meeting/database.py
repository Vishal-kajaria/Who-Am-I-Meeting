from who_am_I_meeting.config import supabase

def save_search(person_name, company_name, meeting_type):
    supabase.table("meeting_history").insert(
        {
            "person_name": person_name,
            "company_name": company_name,
            "meeting_type": meeting_type
        }
    ).execute()

def get_recent_meetings():

    response = (
        supabase.table("meeting_history")
        .select("*")
        .order("created_at", desc=True)
        .limit(10)
        .execute()
    )

    meetings = response.data

    if not meetings:
        return "No meeting history found."

    history_text = "## Recent Meetings\n\n"

    for meeting in meetings:

        history_text += (
            f"- {meeting['person_name']} | "
            f"{meeting['company_name']} | "
            f"{meeting['meeting_type']}\n\n"
        )

    return history_text