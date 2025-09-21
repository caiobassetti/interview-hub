from django.contrib import admin
from .models import Question, Interview, Submission

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "qtype","created_at")
    list_filter = ("qtype",)
    search_fields = ("title", "body", "tags")


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_published", "scheduled_at", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    filter_horizontal = ("questions",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "interview", "question", "metric_score", "submitted_at")
    list_filter = ("interview",)
    search_fields = ("answer_text",)
