from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from groups.models import Group
import misaka
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE, null=True, blank=True )

    def save(self, *args, **kwargs):
        print('###############################################################################hi moood ')
        self.message_html = misaka.html(self.message)
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        super().save(*args, **kwargs)

       


    def __str__(self):
        return self.message

    
    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,'pk':self.pk})


    class Meta():
        ordering = ['-created_at']
        unique_together = ['user', 'message']

class PersonalPost(models.Model):
    author = models.ForeignKey(User, related_name='personalposts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk':self.pk})
        

    def __str__(self):
        return self.title

    class Meta():
        ordering = ['-create_date']
        # unique_together = ['author', 'title']