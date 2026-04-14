from django.db import models

class ResearchReport(models.Model):
    # User ne jo topic diya tha
    task = models.CharField(max_length=500)
    
    # Planner ne jo points banaye (JSON format mein save karenge)
    plan = models.JSONField(default=list, blank=True)
    
    # Final Markdown Report
    final_report = models.TextField(blank=True)
    
    # Status track karne ke liye
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task} - {self.status}"

    class Meta:
        ordering = ['-created_at']