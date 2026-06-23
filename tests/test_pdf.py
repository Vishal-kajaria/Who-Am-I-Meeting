
from who_am_I_meeting.pdf import generate_pdf

def test_pdf_returns_correct_filename():
    result = generate_pdf("testing content","Google")
    assert result == "Google_meeting_brief.pdf"

def test_pdf_filename_with_spaces():
    result = generate_pdf("testing spaces","Google India")
    assert result == "Google_India_meeting_brief.pdf"