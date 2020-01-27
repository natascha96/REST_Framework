from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token
from api.views import (
    VocabularyStatusAPIView,VocabularyDetailAPIView, VocabularyAPIView,
    VocabularyListAPIView, VocabularyDetailListAPIView,
)

app_name = "vocabulary_trainer"

urlpatterns = [
    # Paths for login, register, prof
    path('rest-auth/', include('rest_auth.urls')),
    # /api/rest-auth for registration
    # /api/rest-auth/login/ for login
    # /api/rest-auth/logout/ for logout
    path('rest-auth', include('rest_auth.registration.urls')),

    #http://127.0.0.1:8000/api/refresh-token --> for refreshing token
    path('refresh-token', refresh_jwt_token),

    # Vokabeln
    # Fetch all lists or create a new one
    path('lists/', VocabularyListAPIView.as_view()),

    # Update a single list and delete one
    path('lists/<int:id>/', VocabularyDetailListAPIView.as_view()),

    # Fetch all vocabs of a list or creat a new vocab
    path('vokabeln/', VocabularyAPIView.as_view()),

    # Update a vocab or delete one
    path('vokabeln/<int:id>/', VocabularyDetailAPIView.as_view()),

    # Status der Vokabeln abfragen
    path('vokabelstatus/<int:id>/', VocabularyStatusAPIView.as_view()),
]
