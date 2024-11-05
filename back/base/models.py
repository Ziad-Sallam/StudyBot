from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=50)

    # Human-readable string representation
    def __str__(self):
        return self.name

class Assignment(models.Model): 
    subject_tag = models.ForeignKey(Subject, on_delete=models.CASCADE)  # On deleting a subject, the associated assignments will also be deleted
    
    types = [
        ('sheet_assignment', 'Sheet'),
        ('lab_assignment', 'Lab'),
        ('quiz_assignment', 'Quiz'),
        ('custom_assignment', 'Custom'),  # Allows for a custom type entry
    ]
    type_tag = models.CharField(max_length=20, choices=types, default='custom')
    custom_type = models.CharField(max_length=20, blank=True, null=True)
    
    # In case custom is chosen but not defined
    def clean(self):
        if self.type_tag == 'custom_assignment' and not self.custom_type:
            raise ValidationError('Custom type must be specified when type is custom.')

    # Return human-readable name for assignment type
    def __str__(self):
        return f"{self.get_type_tag_display()} - {self.subject_tag.name}"