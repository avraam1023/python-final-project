from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import Count

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(
        max_length=13, 
        unique=True, 
        validators=[
                RegexValidator(regex=r'^\d{10}|\d{13}$', 
                message="ISBN must be either 10 or 13 digits long.")])
    
    published_year = models.PositiveSmallIntegerField()
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books')

    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def top_liked_books(cls):
        return cls.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

    
    def total_likes(self):
        return self.likes.count()

    class Meta:
        db_table = 'books'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.book}'  

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'book')

class Genre(models.Model):
    name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genre'