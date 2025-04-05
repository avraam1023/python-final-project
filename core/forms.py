from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Genre

class AuthorCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)   
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'isbn', 'genre', 'price', 'published_year')


class GenreForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Genre
        fields = ('name',)

class SearchForm(forms.Form):
    title = forms.CharField(required=False, max_length=100)
    author = forms.CharField(required=False, max_length=100)
    isbn = forms.CharField(required=False, max_length=13)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    published_year = forms.IntegerField(required=False)