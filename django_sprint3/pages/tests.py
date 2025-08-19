from django.test import TestCase
from django.core import mail
from django.core.mail import send_mail

class EmailTest(TestCase):
    def test_send_email(self):
        """Отправляем email"""
        send_mail(
            'Тема',
            'Текст письма.',
            'from@example.com',
            ['to@example.com'],
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Тема')
