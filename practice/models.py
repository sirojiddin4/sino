from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
    """Model to store tests consisting of multiple reading passages"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ReadingPassage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_short = models.BooleanField(default=False)
    # Add passage number (1, 2, or 3) to indicate which IELTS reading passage it is
    passage_number = models.IntegerField(choices=[(1, 'Passage 1'), (2, 'Passage 2'), (3, 'Passage 3')], default=1)
    # Add relation to Test
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='passages', null=True, blank=True)
    
    def __str__(self):
        return self.title

class QuestionType(models.Model):
    """Model to define different question types and their characteristics"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    frontend_type = models.CharField(max_length=100, help_text="Type of UI component to use in frontend")
    instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class QuestionGroup(models.Model):
    """Model to group questions based on question types for a specific passage"""
    title = models.CharField(max_length=200)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='question_groups')
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='question_groups')
    # Add specific instructions for this group (optional, can override type instructions)
    specific_instructions = models.TextField(blank=True, null=True)
    # Add order for displaying the groups
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        # Add a unique constraint to ensure each passage-question_type combination is unique
        unique_together = ['passage', 'question_type']
    
    def __str__(self):
        return f"{self.title} - {self.question_type.name}"
    
    @property
    def instructions(self):
        """Return group-specific instructions if available, otherwise return type instructions"""
        if self.specific_instructions:
            return self.specific_instructions
        return self.question_type.instructions

class Question(models.Model):
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='questions')
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.TextField()
    # Add order number to show the question's order within the group
    order_number = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['question_group__order', 'order_number']
    
    def __str__(self):
        return f"Question {self.order_number} for {self.passage.title}"
    
    @property
    def question_type(self):
        """Return the question type from the question group"""
        return self.question_group.question_type
    
    def save(self, *args, **kwargs):
        # Ensure the question's passage matches the question group's passage
        if self.passage != self.question_group.passage:
            raise ValueError("Question's passage must match question group's passage")
        super().save(*args, **kwargs)

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class PracticeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    # For individual passage practice
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, null=True, blank=True)
    # For full test practice
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    current_passage_number = models.IntegerField(default=1)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    def __str__(self):
        if self.test:
            return f"{self.user.username}'s test {self.test.title} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"
        else:
            return f"{self.user.username}'s practice on {self.start_time.strftime('%Y-%m-%d %H:%M')}"
            
    @property
    def is_full_test(self):
        return self.test is not None

class UserAnswer(models.Model):
    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    marked_for_review = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Answer for {self.question}"

# Chat models remain unchanged

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