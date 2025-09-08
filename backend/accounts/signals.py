from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    # 유저 생성 시 프로필이 없으면 생성
    if created:
        Profile.objects.get_or_create(user=instance)
