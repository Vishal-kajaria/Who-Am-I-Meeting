import pytest
from who_am_I_meeting.pdf import generate_pdf

@pytest.mark.parametrize("company,expected_filename",
                         [("Google","Google_meeting_brief.pdf"),
                          ("Apple India","Apple_India_meeting_brief.pdf"),
                          ("Youtube India Creators","Youtube_India_Creators_meeting_brief.pdf")])
def test_pdf_filename_formats(company, expected_filename):
    result = generate_pdf("test content", company)
    assert result == expected_filename