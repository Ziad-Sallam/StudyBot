from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class Subject(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,default=1)
    type = models.ForeignKey(
        "AssignmentType",
        on_delete=models.CASCADE,
        default=1  # Replace `1` with an appropriate value from your database
    )

class AssignmentType(models.Model):
    type = models.CharField(max_length=20, unique=True)

class AssignmentStatus(models.Model):
    status = models.CharField(max_length=30)

class UserAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Referencing built-in User model
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)
    status = models.ForeignKey("AssignmentStatus", on_delete=models.CASCADE)
    def __str__(self):
        return f"user : {self.user.username} for assignment number : {self.assignment.id} for subject : {self.assignment.subject} status : {self.status.status}"

class Tasks(models.Model):
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Referencing built-in User model
    flag = models.BooleanField()

class Materials(models.Model):
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    file = models.FileField(upload_to='library/')