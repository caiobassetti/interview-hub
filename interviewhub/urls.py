from django.urls import path
from . import views

urlpatterns = [
    path("whoami/", views.whoami, name="whoami"),
    path("questions/", views.QuestionListCreateView.as_view(), name="question-list"),
    path("questions/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"),
]
