from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile
import numpy as np
from .models import EmotionLog, UserSession, UserProfile
from .serializers import EmotionLogSerializer, UserSessionSerializer, UserProfileSerializer
from ml_models.facial_emotion import facial_detector


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
        Expected data: 
        - 'image': uploaded image file (for facial detection)
        - 'source': 'face' or 'voice'
        - 'session_id': (optional) ID of current session
        """
        source = request.data.get('source', 'face')
        
        if source == 'face':
            return self._detect_facial_emotion(request)
        elif source == 'voice':
            return self._detect_voice_emotion(request)
        else:
            return Response(
                {'error': 'Invalid source. Use "face" or "voice"'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _detect_facial_emotion(self, request):
        """
        Handle facial emotion detection from uploaded image
        """
        # Check if image was uploaded
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image file provided. Please upload an image.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        
        # Validate file type
        allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp']
        file_extension = image_file.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            return Response(
                {'error': f'Invalid file type. Allowed: {', '.join(allowed_extensions)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save uploaded file temporarily
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
                for chunk in image_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            # Detect emotion using ML model
            result = facial_detector.detect_from_image(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            # Check if detection was successful
            if not result.get('face_detected', False):
                return Response({
                    'error': result.get('error', 'No face detected in image'),
                    'emotion': 'neutral',
                    'confidence': 0.0,
                    'face_detected': False
                }, status=status.HTTP_200_OK)
            
            # Create emotion log
            session_id = request.data.get('session_id')
            session = None
            
            if session_id:
                try:
                    session = UserSession.objects.get(id=session_id, user=request.user, is_active=True)
                except UserSession.DoesNotExist:
                    pass
            
            # Convert numpy types to Python native types for JSON serialization
            all_emotions = result.get('all_emotions', {})
            all_emotions_serializable = {
                emotion: float(score) for emotion, score in all_emotions.items()
            }
            
            emotion_log = EmotionLog.objects.create(
                user=request.user,
                emotion_type=result['emotion'],
                confidence=float(result['confidence']),
                source='face',
                session=session,
                raw_data=all_emotions_serializable
            )
            
            # Return response
            return Response({
                'id': emotion_log.id,
                'emotion': result['emotion'],
                'confidence': float(result['confidence']),
                'face_detected': True,
                'all_emotions': all_emotions_serializable,
                'timestamp': emotion_log.timestamp,
                'session_id': session.id if session else None
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Clean up on error
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            
            return Response(
                {'error': f'Error processing image: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _detect_voice_emotion(self, request):
        """
        Handle voice emotion detection (placeholder for future implementation)
        """
        return Response({
            'message': 'Voice emotion detection - Coming soon',
            'emotion': 'neutral',
            'confidence': 0.0
        }, status=status.HTTP_501_NOT_IMPLEMENTED)


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
