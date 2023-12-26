from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_old_question_was_not_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(days=2)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.was_published_recently())

    def test_new_question_was_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(hours=12)
        question = Question(pub_date=pub_date)
        self.assertTrue(question.was_published_recently())

    def test_future_question_was_not_published_recently(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.was_published_recently())


def create_question(question_text, days):
    pub_date = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date,
                                   status=Question.Status.APPROVED)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

    def test_future_question_and_past_question(self):
        past_question = create_question('past', -30)
        create_question('future', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        question = create_question('future', 5)
        response = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question = create_question('Past Question.', -5)
        response = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertContains(response, question.question_text)
