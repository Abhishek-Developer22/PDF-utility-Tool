import os
import pytest
from django.conf import settings
from pdf_tool.services import merge_pdfs, extract_pages
from PyPDF2 import PdfWriter, PdfReader

@pytest.fixture(autouse=True)
def media_root_tmp(tmp_path, monkeypatch):
    """Create a temporary MEDIA_ROOT for each test."""
    monkeypatch.setattr(settings, "MEDIA_ROOT", str(tmp_path))
    monkeypatch.setattr(settings, "MEDIA_URL", "/media/")
    yield

def _create_blank_pdf(path, pages=1):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)

def test_merge_two_pdfs(tmp_path):
    a_path = os.path.join(tmp_path, "a.pdf")
    b_path = os.path.join(tmp_path, "b.pdf")
    _create_blank_pdf(a_path, pages=1)
    _create_blank_pdf(b_path, pages=1)
    merged_url = merge_pdfs([a_path, b_path])
    merged_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(merged_url))
    assert os.path.exists(merged_path)
    reader = PdfReader(merged_path)
    assert len(reader.pages) == 2

def test_extract_page_range(tmp_path):
    src_path = os.path.join(tmp_path, "src.pdf")
    _create_blank_pdf(src_path, pages=5)
    extracted_url = extract_pages(src_path, "2-4")
    extracted_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(extracted_url))
    assert os.path.exists(extracted_path)
    reader = PdfReader(extracted_path)
    assert len(reader.pages) == 3
