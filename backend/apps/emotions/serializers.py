from rest_framework import serializers
from .models import EmotionLog, UserSession, UserProfile


class EmotionDetectionSerializer(serializers.Serializer):
    """Serializer for emotion detection requests"""
    image = serializers.ImageField(required=False, help_text="Image file for facial emotion detection")
    audio = serializers.FileField(required=False, help_text="Audio file for voice emotion detection")
    source = serializers.ChoiceField(choices=['face', 'voice'], required=True)
    session_id = serializers.IntegerField(required=False, help_text="Optional session ID to associate with")
    
    def validate(self, data):
        """Validate that appropriate file is provided for the source"""
        source = data.get('source')
        
        if source == 'face' and 'image' not in data:
            raise serializers.ValidationError("Image file is required for facial emotion detection")
        
        if source == 'voice' and 'audio' not in data:
            raise serializers.ValidationError("Audio file is required for voice emotion detection")
        
        return data


class EmotionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionLog
        fields = ['id', 'emotion_type', 'confidence', 'source', 'timestamp', 'raw_data']
        read_only_fields = ['id', 'timestamp']


class UserSessionSerializer(serializers.ModelSerializer):
    emotions = EmotionLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserSession
        fields = ['id', 'start_time', 'end_time', 'is_active', 'dominant_emotion', 
                  'average_confidence', 'total_emotions_detected', 'emotions']
        read_only_fields = ['id', 'start_time', 'end_time', 'dominant_emotion', 
                            'average_confidence', 'total_emotions_detected']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'preferred_music_genre', 'enable_voice_detection', 
                  'enable_face_detection', 'total_sessions']
        read_only_fields = ['id', 'total_sessions']
