from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from api.views import (
    VocabularyStatusAPIView,VocabularyDetailAPIView, VocabularyAPIView,
    VocabularyListAPIView, VocabularyDetailListAPIView,
)
app_name = "api"
schema_view = get_swagger_view(title="Vokabeltrainer API Dokumentation")

urlpatterns = [
    path('documentation/', schema_view),
    # Paths for login, register, prof
    path('', include('rest_auth.urls')),
    # /api/ for registration
    # /api/login/ for login
    # /api/logout/ for logout
    path('registration/', include('rest_auth.registration.urls')),
    # api/refresh-token --> for refreshing token
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
