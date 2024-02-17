from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


def create_question(question_text, pub_date=None, status=Question.Status.APPROVED,
                    choice_texts=None) -> Question:
    if pub_date is None:
        pub_date = timezone.now() - timedelta(days=1)
    if choice_texts is None:
        choice_texts = ['Yes', 'No']

    question = Question.objects.create(question_text=question_text,
                                       pub_date=pub_date, status=status)
    for choice_text in choice_texts:
        question.choices.create(choice_text=choice_text)

    return question


class QuestionViewTest(TestCase):
    def test_empty_question_list(self):
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['count'], 0)
        self.assertEquals(data['results'], [])

    def test_question_list(self):
        create_question('Text1', pub_date=timezone.now() - timedelta(minutes=1))
        create_question('Text2', pub_date=timezone.now() - timedelta(minutes=2))

        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['count'], 2)
        self.assertEquals(data['results'][0]['question_text'], 'Text1')
        self.assertEquals(data['results'][1]['question_text'], 'Text2')

    def test_nonexistent_question_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assertEquals(response.status_code, 404)

    def test_question_detail(self):
        question = create_question(question_text='Text1')

        response = self.client.get(f'/api/questions/{question.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['question_text'], question.question_text)
