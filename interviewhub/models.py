from django.conf import settings
from django.db import models

class Question(models.Model):
    MULTIPLE_CHOICE = "Multiple Choice"
    OPEN_ENDED = "Open Ended"
    SCALE = "Scale"

    QUESTION_TYPES = [
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (OPEN_ENDED, "Open Ended"),
        (SCALE, "Scale (1-5)"),
    ]

    # Question attrs
    title = models.CharField(max_length=200, help_text="Short prompt shown to participants.")
    body = models.TextField(blank=True, help_text="Longer guidance or context.")
    qtype = models.CharField(max_length=16, choices=QUESTION_TYPES, default=OPEN_ENDED)
    tags = models.JSONField(default=list, blank=True)
    options = models.JSONField(default=list, blank=True, help_text="For Multiple Choice: ['A', 'B', ...]")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.qtype}] {self.title}"

class Interview(models.Model):
    CONF_PUBLIC = "public"
    CONF_INTERNAL = "internal"
    CONF_ANON = "anonymous"

    CONF_CHOICES = [
        (CONF_PUBLIC, "Public results"),
        (CONF_INTERNAL, "Internal only"),
        (CONF_ANON, "Anonymous outputs"),
    ]

    # Interview attrs
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_interviews")
    title = models.CharField("Session title", max_length=200)
    description = models.TextField(blank=True, help_text="Guidance shown to participants")
    questions = models.ManyToManyField(Question, related_name="interviews", blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False, help_text="Visible to participants if enabled.")
    confidentiality = models.CharField(max_length=16, choices=CONF_CHOICES, default=CONF_INTERNAL, help_text="How outputs are shared.")
    project_code = models.CharField(max_length=64, blank=True, help_text="Engagement or project code.")
    allowed_participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="invited_interviews", blank=True, help_text="Empty = any authenticated user.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Submission(models.Model):
    # Submission attrs
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions", verbose_name="Participant")
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="submissions", verbose_name="Session")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")
    answer_text = models.TextField(blank=True)
    metric_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Sentiment/LLM score")
    is_anonymous = models.BooleanField(default=False)
    consent_given = models.BooleanField(default=False)
    meta = models.JSONField(default=dict, blank=True, help_text="Freeform context (dept, office, role)")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("candidate", "interview", "question")]
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Submission(user={self.candidate_id}, q={self.question_id})"
