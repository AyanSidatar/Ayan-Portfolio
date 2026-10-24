from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Message


class ContactFormTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            "name": "Recruiter Name",
            "email": "recruiter@example.com",
            "message": "Hi Ayan, we have a Django role open. Are you available?",
            "website": "",
        }
        data.update(overrides)
        return data

    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse("contact"), self.valid_data())
        self.assertRedirects(response, "/#contact", fetch_redirect_response=False)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().name, "Recruiter Name")

    def test_honeypot_blocks_bots(self):
        response = self.client.post(reverse("contact"), self.valid_data(website="http://spam"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Message.objects.count(), 0)

    def test_short_message_is_rejected(self):
        response = self.client.post(reverse("contact"), self.valid_data(message="hi"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Message.objects.count(), 0)

    def test_invalid_email_is_rejected(self):
        response = self.client.post(reverse("contact"), self.valid_data(email="not-an-email"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Message.objects.count(), 0)

    def test_get_is_not_allowed(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 405)

    @override_settings(CONTACT_NOTIFY_EMAIL="owner@example.com")
    def test_owner_is_notified_when_configured(self):
        self.client.post(reverse("contact"), self.valid_data())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["owner@example.com"])

    @override_settings(CONTACT_NOTIFY_EMAIL="")
    def test_no_email_when_not_configured(self):
        self.client.post(reverse("contact"), self.valid_data())
        self.assertEqual(len(mail.outbox), 0)
