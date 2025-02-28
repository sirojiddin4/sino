from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class MotherTongue(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mother_tongue = models.ForeignKey(MotherTongue, on_delete=models.SET_NULL, null=True, blank=True)
    avg_ielts_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    practice_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    selected_coach = models.ForeignKey('core.Coach', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()