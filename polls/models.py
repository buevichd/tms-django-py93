from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Question(models.Model):
    class Status(models.TextChoices):
        NEW = 'NW', _('New')
        REJECTED = 'RJ', _('Rejected')
        APPROVED = 'AP', _('Approved')

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Publication date')
    status = models.CharField(max_length=2, choices=Status, default=Status.NEW)

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='choices',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.question_text} - {self.choice_text}'
