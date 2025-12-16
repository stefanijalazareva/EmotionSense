# EmotionSense

An AI-powered application for facial and voice emotion detection with an intelligent chatbot and emotion-based recommendations, focusing on mental well-being.

## Features

- **Facial Emotion Detection**: Real-time emotion recognition using OpenCV and DeepFace
- **Voice Emotion Detection**: Speech emotion analysis using Librosa and SpeechBrain
- **AI Chatbot**: Context-aware conversational assistant with emotion understanding
- **Personalized Recommendations**: Emotion-based suggestions for well-being improvement

## Tech Stack

### Backend
- Python 3.x
- Django (Web Framework + Templates)
- PostgreSQL (Database)
- Django REST Framework (API endpoints)

### Frontend
- Django Templates
- TailwindCSS (Styling)
- JavaScript (Real-time interactions)

### Machine Learning
- OpenCV + DeepFace (Facial emotion detection)
- Librosa + SpeechBrain (Voice emotion detection)
- TensorFlow/PyTorch (ML framework)
- HuggingFace Transformers (NLP)
- OpenAI API (Chatbot intelligence)

### DevOps
- Git (Version control)
- Docker (Containerization)
- PostgreSQL (Production database)

## Project Structure

```
EmotionSense/
├── backend/                    # Django application
│   ├── config/                # Django settings
│   ├── apps/
│   │   ├── emotions/          # Emotion detection module
│   │   ├── chatbot/           # Chatbot module
│   │   └── recommendations/   # Recommendations module
│   ├── ml_models/             # ML model implementations
│   ├── templates/             # Django templates
│   ├── static/                # Static files (CSS, JS, images)
│   └── manage.py
├── models/                    # Trained ML models (gitignored)
├── data/                      # Training/test data (gitignored)
├── docs/                      # Documentation
├── docker/                    # Docker configuration
└── requirements.txt           # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Git

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd EmotionSense
```

2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up database
```bash
# Configure PostgreSQL connection in .env
python manage.py migrate
```

5. Run development server
```bash
python manage.py runserver
```
