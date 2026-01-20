from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Recommendation(models.Model):
    """Stores recommendation content for different emotions"""
    
    CONTENT_TYPE_CHOICES = [
        ('text', 'Motivational Text'),
        ('music', 'Music/Song'),
        ('activity', 'Activity Suggestion'),
        ('quote', 'Inspirational Quote'),
    ]
    
    EMOTION_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('fear', 'Fear'),
        ('surprise', 'Surprise'),
        ('disgust', 'Disgust'),
        ('neutral', 'Neutral'),
        ('worried', 'Worried'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    emotion_trigger = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    
    # Content details
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Main content: text, lyrics, description")
    
    # For music recommendations
    artist = models.CharField(max_length=100, blank=True)
    spotify_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # For activities
    duration_minutes = models.IntegerField(null=True, blank=True, help_text="Estimated duration for activity")
    difficulty = models.CharField(max_length=20, blank=True, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_count = models.IntegerField(default=0, help_text="How many times this was recommended")
    
    class Meta:
        ordering = ['-usage_count', 'emotion_trigger']
        indexes = [
            models.Index(fields=['emotion_trigger', 'content_type']),
        ]
    
    def __str__(self):
        return f"{self.content_type} for {self.emotion_trigger}: {self.title}"


class UserRecommendationHistory(models.Model):
    """Tracks recommendations given to users"""
    
    FEEDBACK_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('neutral', 'Neutral'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_history')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='history')
    
    # Context
    detected_emotion = models.CharField(max_length=20)
    emotion_confidence = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # User interaction
    was_clicked = models.BooleanField(default=False)
    was_completed = models.BooleanField(default=False, help_text="For activities: did user complete it?")
    user_feedback = models.CharField(max_length=20, choices=FEEDBACK_CHOICES, null=True, blank=True)
    feedback_comment = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User Recommendation History'
        verbose_name_plural = 'User Recommendation Histories'
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['recommendation']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.recommendation.title} at {self.timestamp}"


class EmotionInsight(models.Model):
    """Stores insights and patterns about user's emotional state"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_insights')
    
    # Time period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Insights
    most_common_emotion = models.CharField(max_length=20)
    emotion_distribution = models.JSONField(help_text="Distribution of emotions over period")
    mood_trend = models.CharField(max_length=20, choices=[
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
    ])
    
    # Recommendations summary
    most_helpful_content_type = models.CharField(max_length=20, blank=True)
    total_recommendations_received = models.IntegerField(default=0)
    
    # Auto-generated insights
    ai_summary = models.TextField(blank=True, help_text="AI-generated summary of emotional patterns")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-end_date']
        verbose_name = 'Emotion Insight'
        verbose_name_plural = 'Emotion Insights'
    
    def __str__(self):
        return f"{self.user.username} - Insights {self.start_date} to {self.end_date}"
