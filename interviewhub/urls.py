from django.urls import path

from . import views

urlpatterns = [
    path("whoami/", views.WhoAmIView.as_view(), name="whoami"),
    path("questions/", views.QuestionListCreateView.as_view(), name="question-list"),
    path("questions/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"),
    path("submissions/", views.SubmissionListView.as_view(), name="submissions"),
    path("submissions/create/", views.SubmissionCreateView.as_view(), name="submission-create"),
    path("interviews/", views.InterviewListCreateView.as_view(), name="interview-list"),
    path("interviews/<int:pk>/", views.InterviewDetailView.as_view(), name="interview-detail"),
]
