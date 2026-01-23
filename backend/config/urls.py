"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/emotions/', include('apps.emotions.urls')),
    path('api/chatbot/', include('apps.chatbot.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
    
    # Frontend
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('emotion-detect/', TemplateView.as_view(template_name='emotion_detect.html'), name='emotion_detect'),
    path('chatbot/', TemplateView.as_view(template_name='chatbot.html'), name='chatbot'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('test-emotion/', TemplateView.as_view(template_name='test_emotion.html'), name='test_emotion'),
]
