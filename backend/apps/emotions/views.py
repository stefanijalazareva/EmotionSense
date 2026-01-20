from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EmotionLog, UserSession, UserProfile
from .serializers import EmotionLogSerializer, UserSessionSerializer, UserProfileSerializer


class EmotionLogViewSet(viewsets.ModelViewSet):
    """API endpoint for emotion logs"""
    serializer_class = EmotionLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmotionLog.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def detect(self, request):
        """
        Detect emotion from uploaded image or audio
        Expected data: {'source': 'face/voice', 'data': file_or_data}
        """
        # Placeholder - will implement ML logic later
        return Response({
            'message': 'Emotion detection endpoint - ML implementation pending',
            'emotion': 'neutral',
            'confidence': 0.0
        })


class UserSessionViewSet(viewsets.ModelViewSet):
    """API endpoint for user sessions"""
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End a session and calculate statistics"""
        session = self.get_object()
        session.end_session()
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get or create active session"""
        session, created = UserSession.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        serializer = self.get_serializer(session)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for user profiles"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
