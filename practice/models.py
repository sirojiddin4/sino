from django.db import models
from django.contrib.auth.models import User

class ReadingPassage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_short = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('short_answer', 'Short Answer'),
    )
    
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    correct_answer = models.TextField()
    
    def __str__(self):
        return f"Question for {self.passage.title}"

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class PracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s practice on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class UserAnswer(models.Model):
    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    marked_for_review = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Answer for {self.question}"

# Add these to your existing practice/models.py file

class ChatConversation(models.Model):
    """Model to store chat conversations between users and coaches"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def get_display_title(self):
        """Returns a formatted title for display"""
        # Truncate title if too long
        if len(self.title) > 30:
            return self.title[:27] + "..."
        return self.title

class ChatMessage(models.Model):
    """Model to store individual chat messages"""
    SENDER_CHOICES = (
        ('user', 'User'),
        ('coach', 'Coach'),
    )
    
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"