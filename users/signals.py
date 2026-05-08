from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"\n---> DIQQAT! Signal ishladi! Xat quyidagi manzilga jo'natilmoqda: {instance.email} <--- \n")
        subject = "Welcome to Goodreads Clone!"
        message = f"Salom {instance.username}!\n\nBizning saytimizdan ro'yxatdan o'tganingiz uchun tashakkur. Kitoblar olamida sarguzashtingizni boshlang!"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )
