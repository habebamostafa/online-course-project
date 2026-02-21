# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    """Course model - assuming this exists from the base project"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in hours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """Lesson model - assuming this exists from the base project"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(models.Model):
    """Question model for assessments"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title[:30]}... - Q{self.order}: {self.question_text[:50]}..."

class Choice(models.Model):
    """Choice model for question options"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.choice_text[:30]}..."

class Submission(models.Model):
    """Submission model for storing exam attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions')
    score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - Score: {self.score}%"

    def calculate_score(self):
        """Calculate the score based on selected correct choices"""
        total_questions = self.course.questions.count()
        if total_questions == 0:
            return 0
        
        selected_choices = self.choices.all()
        correct_count = selected_choices.filter(is_correct=True).count()
        self.score = (correct_count / total_questions) * 100
        self.save()
        return self.score