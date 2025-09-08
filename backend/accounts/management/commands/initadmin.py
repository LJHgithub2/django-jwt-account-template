# accounts/management/commands/initadmin.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a superuser from env vars if it does not exist (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_USERNAME/PASSWORD not set; skip creating superuser."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' already exists. Skipping."
            ))
            return

        User.objects.create_superuser(username=username, email=email or "", password=password)
        self.stdout.write(self.style.SUCCESS(
            f"Superuser '{username}' created."
        ))
