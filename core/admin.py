from django.contrib import admin
from .models import Book, Like, Genre

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Like)