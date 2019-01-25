from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # One-to-one relationship with User table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmation = models.BooleanField(default=False)
    score = models.IntegerField(default=100)

    distance = models.FloatField(default=0)
    leaps = models.FloatField(default=0)
    heart_rate = models.IntegerField(default=0)

    target_distance = models.FloatField(null=True)
    target_leaps = models.FloatField(null=True)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.FloatField()
    leap_count = models.FloatField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
