from django.db import models
from django.urls import reverse
from django.utils import timezone
from posts.models import PersonalPost
from django.contrib.auth import  get_user_model
User= get_user_model()


# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(PersonalPost, related_name='comments', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        #or self.pk PersonalPost
        return reverse('personalpost:post_detail', kwargs={'pk':self.pk})


