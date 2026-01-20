from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, ChatMessage, ChatbotContext
from .serializers import ChatSessionSerializer, ChatMessageSerializer, ChatbotContextSerializer


class ChatSessionViewSet(viewsets.ModelViewSet):
    """API endpoint for chat sessions"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get or create active chat session"""
        session, created = ChatSession.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End a chat session"""
        session = self.get_object()
        session.end_session()
        serializer = self.get_serializer(session)
        return Response(serializer.data)


class ChatMessageViewSet(viewsets.ModelViewSet):
    """API endpoint for chat messages"""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """
        Send a message and get bot response
        Expected data: {'message': 'user message', 'emotion': 'detected_emotion'}
        """
        user_message = request.data.get('message')
        detected_emotion = request.data.get('emotion')
        
        # Get or create active session
        session, _ = ChatSession.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        
        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=user_message,
            detected_emotion=detected_emotion
        )
        
        # Generate bot response (placeholder - will implement AI later)
        bot_response = self._generate_bot_response(user_message, detected_emotion)
        
        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='bot',
            message=bot_response,
            response_type='general'
        )
        
        return Response({
            'user_message': ChatMessageSerializer(user_msg).data,
            'bot_message': ChatMessageSerializer(bot_msg).data
        })
    
    def _generate_bot_response(self, message, emotion):
        """Placeholder for AI-generated response"""
        responses = {
            'sad': "I'm here to listen. Would you like to talk about what's making you feel this way?",
            'worried': "It's normal to feel worried sometimes. Let's work through this together.",
            'angry': "I understand you're upset. Take a deep breath. What's troubling you?",
            'happy': "That's wonderful! I'm glad you're feeling good. What's bringing you joy today?",
        }
        return responses.get(emotion, "I'm here to support you. How can I help you today?")
