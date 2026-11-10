import os
import logging
import logging.config
from django.conf import settings
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('pdf_tool')

from typing import List, Iterable

import uuid
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

def ensure_media_dir() -> None:
    """Ensure that the MEDIA_ROOT directory exists."""
    media_dir = settings.MEDIA_ROOT
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
        logger.info("Created media directory: %s", media_dir)
    else:
        logger.debug("Media directory already exists: %s", media_dir)

def merge_pdfs(file_list: Iterable[str]) -> str:
    """Merge a list of PDF file paths into a single PDF.

    Returns the media URL of the merged PDF.
    """
    logger.info("Merging %d PDF files", len(list(file_list)))
    ensure_media_dir()
    pdf_writer = PdfWriter()

    for file in file_list:
        logger.debug("Reading PDF file: %s", file)
        pdf_reader = PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    output_filename = f"merged_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    with open(output_path, 'wb') as out:
        pdf_writer.write(out)
        logger.info("Merged PDF written to %s", output_path)

    return settings.MEDIA_URL + output_filename

def extract_pages(pdf_file: str, page_range_str: str) -> str:
    """Extract specific pages from a PDF.

    `page_range_str` can be a comma‑separated list of pages and/or ranges,
    e.g. "1,3,5" or "2-8" or "1,4,6-10".
    Returns the media URL of the newly created PDF.
    """
    logger.info("Extracting pages '%s' from %s", page_range_str, pdf_file)
    ensure_media_dir()

    pdf_reader = PdfReader(pdf_file)
    total_pages = len(pdf_reader.pages)
    pages_to_extract = set()

    parts = page_range_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start > end:
                raise ValueError("Invalid range: start page cannot be greater than end page.")
            pages_to_extract.update(range(start, end + 1))
        else:
            pages_to_extract.add(int(part))

    sorted_pages = sorted(pages_to_extract)
    pdf_writer = PdfWriter()
    for p in sorted_pages:
        if 1 <= p <= total_pages:
            pdf_writer.add_page(pdf_reader.pages[p - 1])
        else:
            raise ValueError(f"Page {p} does not exist in the document (total pages: {total_pages}).")

    output_filename = f"extracted_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

    with open(output_path, 'wb') as out:
        pdf_writer.write(out)
        logger.info("Extracted PDF written to %s", output_path)

    return settings.MEDIA_URL + output_filename
