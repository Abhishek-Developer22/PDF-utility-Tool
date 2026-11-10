from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf', 'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class MergeForm(forms.Form):
    files = MultipleFileField(label='Select PDF files to merge', required=True)

    def clean_files(self):
        files = self.cleaned_data.get('files')
        if not files or len(files) < 2:
            raise forms.ValidationError("You must select at least 2 PDF files to merge.")
        for f in files:
            if not f.name.lower().endswith('.pdf'):
                raise forms.ValidationError(f"File {f.name} is not a valid PDF.")
        return files

import re

class ExtractForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file', required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}))
    page_range = forms.CharField(label='Page Numbers/Range', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1,3,5 or 2-8 or 1,4,6-10'}))

    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Uploaded file is not a valid PDF.")
        return file

    def clean_page_range(self):
        page_range = self.cleaned_data.get('page_range')
        page_range = page_range.replace(" ", "")
        pattern = r'^(\d+(-\d+)?,)*\d+(-\d+)?$'
        if not re.match(pattern, page_range):
            raise forms.ValidationError("Invalid format. Use comma-separated numbers or ranges (e.g., 1,3,5 or 2-8)")
        return page_range
