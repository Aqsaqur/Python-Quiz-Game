from django.contrib import admin
from django.urls import path, include 
from .views import QuizViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()  # Note the parentheses here to create an instance
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<int:pk>/add_question/', QuizViewSet.as_view({'post': 'add_question'}), name='add_question')
]