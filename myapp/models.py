from django.db import models

class SequenceAnalysis(models.Model):
    sequence = models.TextField()
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis on {self.created_at}"
