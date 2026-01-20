from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    """Groups related chat messages into a conversation"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Session context
    initial_emotion = models.CharField(max_length=20, null=True, blank=True, help_text="User's emotion at session start")
    total_messages = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - Chat Session {self.id}"
    
    def end_session(self):
        """End the chat session"""
        self.end_time = timezone.now()
        self.is_active = False
        self.total_messages = self.messages.count()
        self.save()


class ChatMessage(models.Model):
    """Stores individual messages in chatbot conversations"""
    
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Emotion context at the time of message
    detected_emotion = models.CharField(max_length=20, null=True, blank=True, help_text="User's emotion when message was sent")
    emotion_confidence = models.FloatField(null=True, blank=True)
    
    # Bot response metadata
    response_type = models.CharField(max_length=50, null=True, blank=True, help_text="Type of bot response: advice, motivation, question, etc.")
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['session', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sender}: {self.message[:50]}..."


class ChatbotContext(models.Model):
    """Stores chatbot conversation context and memory"""
    
    session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name='context')
    
    # Conversation memory (stored as JSON)
    conversation_summary = models.TextField(blank=True, help_text="Summary of conversation so far")
    user_concerns = models.JSONField(default=list, help_text="List of user's expressed concerns")
    suggested_topics = models.JSONField(default=list, help_text="Topics bot has suggested")
    
    # Emotional state tracking
    emotion_history = models.JSONField(default=list, help_text="History of detected emotions during chat")
    mood_trend = models.CharField(max_length=20, null=True, blank=True, help_text="improving, declining, stable")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Context for {self.session}"
