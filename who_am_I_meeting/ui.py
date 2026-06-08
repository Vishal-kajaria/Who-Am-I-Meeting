import gradio as gr
from who_am_I_meeting.search import search_company
from who_am_I_meeting.brief import generate_meeting_brief
from who_am_I_meeting.database import save_search, get_recent_meetings
from who_am_I_meeting.pdf import generate_pdf

def show_loading():

    return (
        "⏳ Generating meeting brief...",
        gr.update(visible=False),
        gr.update(visible=True)
    )

def clear_loading():    
    return ""

def show_history():

    return (
        gr.update(
            value=get_recent_meetings(),
            visible=True
        ),
        gr.update(
            value="",
            visible=False
        )
    )

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

        save_search(name, company, meeting_type)

        pdf_file = generate_pdf(meeting_brief, company)
        
        return meeting_brief, pdf_file
    except Exception as e:
        return f"An error occurred: {str(e)}", None

app = gr.Blocks()

with app:

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
            history_button = gr.Button("Show History")

        with gr.Column(scale=2):
            status_box = gr.Markdown()
            history_box = gr.Markdown(visible=False)
            output_box = gr.Markdown(height=800)

        with gr.Row():
            pdf_output = gr.File(label="Download Meeting Brief")

    generate_button.click(
        fn=show_loading,
        outputs=[status_box, history_box, output_box]
    ).then(
        fn=who_am_i_meeting,
        inputs=[name_input, company_input, meeting_type],
        outputs=[output_box, pdf_output]
    ).then(
        fn=clear_loading,
        outputs=status_box
    )
    history_button.click(
        fn=show_history,
        outputs=[history_box, output_box]
    )