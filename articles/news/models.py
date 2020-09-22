from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    full_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

   

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:article-detail", kwargs={"pk": self.pk})



class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_body

    def get_absolute_url(self):
        return reverse("news:article-detail", kwargs={"pk": self.pk})
