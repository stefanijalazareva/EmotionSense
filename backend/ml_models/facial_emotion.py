"""
Facial Emotion Detection Module using OpenCV and DeepFace
"""
import cv2
from deepface import DeepFace
import numpy as np
from typing import Dict, Optional


class FacialEmotionDetector:
    """Detects emotions from facial images using DeepFace"""
    
    def __init__(self):
        self.emotion_mapping = {
            'angry': 'angry',
            'disgust': 'disgust',
            'fear': 'fear',
            'happy': 'happy',
            'sad': 'sad',
            'surprise': 'surprise',
            'neutral': 'neutral'
        }
    
    def detect_from_image(self, image_path: str) -> Dict[str, any]:
        """
        Detect emotion from an image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with emotion, confidence, and raw data
        """
        try:
            # Analyze face using DeepFace
            result = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False
            )
            
            # Handle both single face and multiple faces
            if isinstance(result, list):
                result = result[0]  # Take first face
            
            # Get dominant emotion
            dominant_emotion = result['dominant_emotion']
            emotion_scores = result['emotion']
            confidence = emotion_scores[dominant_emotion] / 100.0
            
            return {
                'emotion': self.emotion_mapping.get(dominant_emotion, 'neutral'),
                'confidence': confidence,
                'all_emotions': emotion_scores,
                'face_detected': True
            }
            
        except Exception as e:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'error': str(e),
                'face_detected': False
            }
    
    def detect_from_frame(self, frame: np.ndarray) -> Dict[str, any]:
        """
        Detect emotion from a video frame (numpy array)
        
        Args:
            frame: Video frame as numpy array (from cv2)
            
        Returns:
            Dict with emotion, confidence, and raw data
        """
        try:
            # Analyze the frame
            result = DeepFace.analyze(
                img_path=frame,
                actions=['emotion'],
                enforce_detection=False
            )
            
            if isinstance(result, list):
                result = result[0]
            
            dominant_emotion = result['dominant_emotion']
            emotion_scores = result['emotion']
            confidence = emotion_scores[dominant_emotion] / 100.0
            
            return {
                'emotion': self.emotion_mapping.get(dominant_emotion, 'neutral'),
                'confidence': confidence,
                'all_emotions': emotion_scores,
                'face_detected': True
            }
            
        except Exception as e:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'error': str(e),
                'face_detected': False
            }
    
    def detect_from_webcam(self, duration: int = 5) -> Dict[str, any]:
        """
        Capture from webcam and detect emotion
        
        Args:
            duration: Seconds to capture (analyzes last frame)
            
        Returns:
            Dict with emotion detection results
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'error': 'Could not access webcam',
                'face_detected': False
            }
        
        frame = None
        for _ in range(duration * 30):  # Assuming 30fps
            ret, frame = cap.read()
            if not ret:
                break
        
        cap.release()
        
        if frame is not None:
            return self.detect_from_frame(frame)
        else:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'error': 'Could not capture frame',
                'face_detected': False
            }


# Singleton instance
facial_detector = FacialEmotionDetector()
