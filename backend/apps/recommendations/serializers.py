from rest_framework import serializers
from .models import Recommendation, UserRecommendationHistory, EmotionInsight


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'content_type', 'emotion_trigger', 'title', 'content', 
                  'artist', 'spotify_url', 'youtube_url', 'duration_minutes', 
                  'difficulty', 'usage_count']
        read_only_fields = ['id', 'usage_count']


class UserRecommendationHistorySerializer(serializers.ModelSerializer):
    recommendation_detail = RecommendationSerializer(source='recommendation', read_only=True)
    
    class Meta:
        model = UserRecommendationHistory
        fields = ['id', 'recommendation', 'recommendation_detail', 'detected_emotion', 
                  'emotion_confidence', 'timestamp', 'was_clicked', 'was_completed', 
                  'user_feedback', 'feedback_comment']
        read_only_fields = ['id', 'timestamp']


class EmotionInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionInsight
        fields = ['id', 'start_date', 'end_date', 'most_common_emotion', 
                  'emotion_distribution', 'mood_trend', 'most_helpful_content_type', 
                  'total_recommendations_received', 'ai_summary', 'created_at']
        read_only_fields = ['id', 'created_at']
