from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Publication date')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='choices',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.question_text} - {self.choice_text}'
