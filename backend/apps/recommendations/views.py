from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Recommendation, UserRecommendationHistory, EmotionInsight
from .serializers import RecommendationSerializer, UserRecommendationHistorySerializer, EmotionInsightSerializer
import random


class RecommendationViewSet(viewsets.ModelViewSet):
    """API endpoint for recommendations"""
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Recommendation.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def for_emotion(self, request):
        """
        Get recommendations for a specific emotion
        Query params: ?emotion=sad&type=music
        """
        emotion = request.query_params.get('emotion', 'neutral')
        content_type = request.query_params.get('type', None)
        
        recommendations = Recommendation.objects.filter(
            emotion_trigger=emotion,
            is_active=True
        )
        
        if content_type:
            recommendations = recommendations.filter(content_type=content_type)
        
        # Get random 3-5 recommendations
        recommendations = random.sample(
            list(recommendations),
            min(5, recommendations.count())
        )
        
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)


class UserRecommendationHistoryViewSet(viewsets.ModelViewSet):
    """API endpoint for user recommendation history"""
    serializer_class = UserRecommendationHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserRecommendationHistory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        # Increment recommendation usage count
        recommendation = serializer.validated_data.get('recommendation')
        recommendation.usage_count += 1
        recommendation.save()
    
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """Submit feedback for a recommendation"""
        history = self.get_object()
        history.user_feedback = request.data.get('feedback')
        history.feedback_comment = request.data.get('comment', '')
        history.save()
        
        serializer = self.get_serializer(history)
        return Response(serializer.data)


class EmotionInsightViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for emotion insights"""
    serializer_class = EmotionInsightSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmotionInsight.objects.filter(user=self.request.user)
