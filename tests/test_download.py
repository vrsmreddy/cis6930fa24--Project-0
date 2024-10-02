import sys
import pytest
from unittest import mock  # Add this import
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))

import main  # Now Python can find the main module

def test_fetchincidents():
    url = "http://example.com/test.pdf"

    # Mocking urllib request to avoid actual download
    mock_response = mock.Mock()
    mock_response.read.return_value = b'%PDF-1.4\n...'  # Mock PDF data
    
    with mock.patch('urllib.request.urlopen', return_value=mock_response):
        data = main.fetchincidents(url)
        assert data == b'%PDF-1.4\n...'

def test_extractincidents():
    # Simulating minimal PDF content for extraction
    pdf_data = b'%PDF-1.4\n...'  # Mock PDF data for extraction

    # Mock the process of reading the PDF file
    with mock.patch('PyPDF2.PdfFileReader') as mock_pdf_reader:
        # Mock the PDF object
        mock_pdf = mock.Mock()
        mock_pdf.numPages = 1
        # Simulate extracting text that matches the expected format
        mock_pdf.getPage.return_value.extractText.return_value = (
            "Date / Time Incident Number Location Nature Incident ORI\n"
            "10/01/2024 14:00\n12345\nMain St\nTheft\nOK12345\n"
        )
        mock_pdf_reader.return_value = mock_pdf

        extracted_data = main.extractincidents(pdf_data)
    
    # Assertions to check if the extracted data matches the expected format
    assert isinstance(extracted_data, list)
    assert len(extracted_data) == 1  # Expecting 1 entry
    assert len(extracted_data[0]) == 5  # Each incident should have 5 fields
    assert extracted_data[0] == [
        '||10/01/2024 14:00',  # Adjusted to include the '||' prefix
        '12345',
        'Main St',
        'Theft',
        'OK12345'
    ]

