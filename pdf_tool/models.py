from django.db import models

class Document(models.Model):
    """Model to keep track of uploaded PDFs and generated files."""
    uploaded_file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self) -> str:
        return f"Document {self.id} - {self.uploaded_file.name}"
