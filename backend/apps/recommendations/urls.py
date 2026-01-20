from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, UserRecommendationHistoryViewSet, EmotionInsightViewSet

router = DefaultRouter()
router.register(r'items', RecommendationViewSet, basename='recommendation')
router.register(r'history', UserRecommendationHistoryViewSet, basename='recommendationhistory')
router.register(r'insights', EmotionInsightViewSet, basename='emotioninsight')

urlpatterns = [
    path('', include(router.urls)),
]
