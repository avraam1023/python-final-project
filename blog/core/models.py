from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model) : 
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    text = models.TextField()


class Comments(models.Model) :
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()


