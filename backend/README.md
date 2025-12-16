# EmotionSense Backend

Django backend for EmotionSense application.

## Setup

1. Activate virtual environment (from root):
```bash
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Apps

- **emotions**: Facial and voice emotion detection
- **chatbot**: AI chatbot with emotion awareness
- **recommendations**: Emotion-based recommendations

## API Endpoints

Documentation coming soon...
