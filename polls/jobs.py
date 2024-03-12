from django_rq import job
from django.db.models import F

from polls.models import Question


@job
def update_question_view_count(question: Question):
    question.view_count = F('view_count') + 1
    question.save()
