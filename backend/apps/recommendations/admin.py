from django.contrib import admin
from .models import Recommendation, UserRecommendationHistory, EmotionInsight


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'emotion_trigger', 'usage_count', 'is_active']
    list_filter = ['content_type', 'emotion_trigger', 'is_active']
    search_fields = ['title', 'content', 'artist']
    readonly_fields = ['created_at', 'usage_count']


@admin.register(UserRecommendationHistory)
class UserRecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation', 'detected_emotion', 'timestamp', 'user_feedback', 'was_clicked']
    list_filter = ['detected_emotion', 'user_feedback', 'was_clicked', 'timestamp']
    search_fields = ['user__username', 'recommendation__title']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(EmotionInsight)
class EmotionInsightAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'most_common_emotion', 'mood_trend']
    list_filter = ['most_common_emotion', 'mood_trend', 'end_date']
    search_fields = ['user__username', 'ai_summary']
    readonly_fields = ['created_at']
