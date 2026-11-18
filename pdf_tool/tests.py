import os
import tempfile
from django.test import TestCase, override_settings
from django.conf import settings
from pdf_tool.services import merge_pdfs, extract_pages
from PyPDF2 import PdfWriter, PdfReader


def _create_blank_pdf(path, pages=1):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)


class PDFToolTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.media_root = self.temp_dir.name
        self.settings_override = override_settings(
            MEDIA_ROOT=self.media_root,
            MEDIA_URL='/media/'
        )
        self.settings_override.enable()

    def tearDown(self):
        self.settings_override.disable()
        self.temp_dir.cleanup()

    def test_merge_two_pdfs(self):
        a_path = os.path.join(self.media_root, "a.pdf")
        b_path = os.path.join(self.media_root, "b.pdf")
        _create_blank_pdf(a_path, pages=1)
        _create_blank_pdf(b_path, pages=1)

        merged_url = merge_pdfs([a_path, b_path])
        merged_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(merged_url))
        self.assertTrue(os.path.exists(merged_path))
        reader = PdfReader(merged_path)
        self.assertEqual(len(reader.pages), 2)

    def test_extract_page_range(self):
        src_path = os.path.join(self.media_root, "src.pdf")
        _create_blank_pdf(src_path, pages=5)

        extracted_url = extract_pages(src_path, "2-4")
        extracted_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(extracted_url))
        self.assertTrue(os.path.exists(extracted_path))
        reader = PdfReader(extracted_path)
        self.assertEqual(len(reader.pages), 3)

    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_merge_page_status(self):
        response = self.client.get('/merge/')
        self.assertEqual(response.status_code, 200)

    def test_extract_page_status(self):
        response = self.client.get('/extract/')
        self.assertEqual(response.status_code, 200)
