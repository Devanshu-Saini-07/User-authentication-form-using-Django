from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password=self.password,
            first_name="Existing",
            last_name="User",
        )

    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "AnotherStrongPass123!",
                "password2": "AnotherStrongPass123!",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newuser", email="newuser@example.com").exists())
        messages = list(response.context["messages"])
        self.assertTrue(any("Account created successfully" in str(message) for message in messages))

    def test_login_logout_and_dashboard_protection(self):
        dashboard_url = reverse("dashboard")
        login_url = reverse("accounts:login")

        response = self.client.get(dashboard_url)
        self.assertRedirects(response, f"{login_url}?next={dashboard_url}")

        response = self.client.post(
            login_url,
            {"username": self.user.username, "password": self.password},
            follow=True,
        )
        self.assertRedirects(response, dashboard_url)
        self.assertContains(response, self.user.email)

        response = self.client.post(reverse("accounts:logout"), follow=True)
        self.assertRedirects(response, login_url)

        response = self.client.get(dashboard_url)
        self.assertRedirects(response, f"{login_url}?next={dashboard_url}")

    def test_authenticated_user_is_redirected_away_from_auth_pages(self):
        self.client.login(username=self.user.username, password=self.password)

        login_response = self.client.get(reverse("accounts:login"))
        signup_response = self.client.get(reverse("accounts:signup"))

        self.assertRedirects(login_response, reverse("dashboard"))
        self.assertRedirects(signup_response, reverse("dashboard"))

    def test_profile_edit_updates_user_information(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(
            reverse("accounts:edit_profile"),
            {
                "username": "updateduser",
                "email": "updated@example.com",
                "first_name": "Updated",
                "last_name": "Name",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_password_change_keeps_user_logged_in(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": self.password,
                "new_password1": "NewStrongPass123!",
                "new_password2": "NewStrongPass123!",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPass123!"))

        dashboard_response = self.client.get(reverse("dashboard"))
        self.assertEqual(dashboard_response.status_code, 200)

    def test_password_reset_flow_sends_email_and_resets_password(self):
        response = self.client.post(
            reverse("accounts:password_reset"),
            {"email": self.user.email},
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset", mail.outbox[0].body.lower())

        reset_email = mail.outbox[0]
        reset_path = None
        for line in reset_email.body.splitlines():
            if "/accounts/reset/" in line:
                reset_path = line.strip().split("://", 1)[-1]
                reset_path = "/" + reset_path.split("/", 1)[1]
                break

        self.assertIsNotNone(reset_path)

        confirm_response = self.client.get(reset_path, follow=True)
        self.assertEqual(confirm_response.status_code, 200)

        final_reset_url = confirm_response.redirect_chain[-1][0] if confirm_response.redirect_chain else reset_path
        response = self.client.post(
            final_reset_url,
            {
                "new_password1": "ResetStrongPass123!",
                "new_password2": "ResetStrongPass123!",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("ResetStrongPass123!"))
