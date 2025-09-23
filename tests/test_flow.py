import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_full_flow_create_interview_submit_answers_summarize():
    # Create users
    User.objects.create_user(username="fiona", password="pw", is_staff=True)
    User.objects.create_user(username="alice", password="pw")

    client = APIClient()

    # Get access token
    def token(username, password):
        resp = client.post("/api/auth/token/", {"username": username, "password": password}, format="json")
        assert resp.status_code == 200
        return resp.data["access"]


    fiona_access = token("fiona", "pw")
    alice_access = token("alice", "pw")

    # Create questions
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {fiona_access}")
    q1 = client.post("/api/questions/", {
        "title": "Leadership clarity",
        "qtype": "Scale"
    }, format="json")
    assert q1.status_code == 201
    q1_id = q1.data["id"]

    q2 = client.post("/api/questions/", {
        "title": "Preferred tool",
        "qtype": "Multiple Choice",
        "options": ["Jira","Confluence","Slack"]
    }, format="json")
    assert q2.status_code == 201
    q2_id = q2.data["id"]

    # Create Interview and attach questions
    iv = client.post("/api/interviews/", {
        "title": "Org Health Pulse",
        "description": "Q snapshot",
        "is_published": True,
        "questions": [q1_id, q2_id],
    }, format="json")
    assert iv.status_code == 201
    interview_id = iv.data["id"]

    # Alice submits answers
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {alice_access}")
    s1 = client.post("/api/submissions/create/", {"interview": interview_id, "question": q1_id, "answer_text": "4"}, format="json")
    s2 = client.post("/api/submissions/create/", {"interview": interview_id, "question": q2_id, "answer_text": "Slack"}, format="json")
    assert s1.status_code == 201 and s2.status_code == 201
