from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import MergeForm, ExtractForm
from . import services
import os
from django.conf import settings
import logging
logger = logging.getLogger('pdf_tool')

def home(request):
    return render(request, 'pdf_tool/home.html')

def merge_pdf(request):
    download_url = None
    error_message = None
    
    if request.method == 'POST':
        form = MergeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                files = form.cleaned_data['files']
                download_url = services.merge_pdfs(files)
                logger.info('Merge PDF request processed successfully')
            except Exception as e:
                error_message = str(e)
                logger.error('Error during merge PDF: %s', e)
    else:
        form = MergeForm()
        
    return render(request, 'pdf_tool/merge.html', {
        'form': form,
        'download_url': download_url,
        'error_message': error_message
    })

def extract_pdf(request):
    download_url = None
    error_message = None
    
    if request.method == 'POST':
        form = ExtractForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pdf_file = form.cleaned_data['pdf_file']
                page_range = form.cleaned_data['page_range']
                download_url = services.extract_pages(pdf_file, page_range)
                logger.info('Extract PDF request processed successfully')
            except ValueError as ve:
                error_message = str(ve)
                logger.warning('Invalid page range: %s', ve)
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                logger.error('Error during extract PDF: %s', e)
    else:
        form = ExtractForm()
        
    return render(request, 'pdf_tool/extract.html', {
        'form': form,
        'download_url': download_url,
        'error_message': error_message
    })

def view_logs(request):
    log_path = settings.LOGGING['handlers']['file']['filename']
    try:
        with open(log_path, 'r') as f:
            logs = f.read()
        if not logs.strip():
            logs = "Log file is empty. No entries yet."
    except FileNotFoundError:
        logs = "Log file not found."
    from django.http import HttpResponse
    return HttpResponse(f"<pre>{logs}</pre>")
