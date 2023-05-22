from django.contrib.auth.models import User
from .models import Profile
# from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to Dev Hub'
        message = 'Your profile has been created successfully!\n\n We are glad you have joined the biggest developers\' online Community!\n Please feel free interact with others developers on the platform.\n '

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user=instance.user
        user.delete()
    except User.DoesNotExist:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

