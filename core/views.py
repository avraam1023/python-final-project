from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Book, Genre, Like
from .forms import BookForm, GenreForm, SearchForm, AuthorCreationForm

# Auth
def register_user(request):
    form = AuthorCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'User was successfully registered')
        return redirect('home')

    return render(request, 'core/register.html', {'form': form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request, 
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            messages.success(request, 'User was successfully logged in')
            return redirect('home')
        
        messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')


# Home & Shop
def home(request):
    top_liked_books = Book.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
    return render(request, 'core/index.html', {'books': top_liked_books})



def shop(request):
    form = SearchForm(request.GET)
    query = Q()
    liked_books = []

    if request.user.is_authenticated:
        liked_books = list(Like.objects.filter(user=request.user).values_list('book_id', flat=True))

    if form.is_valid():
        if title := form.cleaned_data.get('title'):
            query |= Q(title__icontains=title)
        if author := form.cleaned_data.get('author'):
            query |= Q(author__username__icontains=author)
        if isbn := form.cleaned_data.get('isbn'):
            query |= Q(isbn__icontains=isbn)
        if genre := form.cleaned_data.get('genre'):
            query |= Q(genre=genre)
        if published_year := form.cleaned_data.get('published_year'):
            query |= Q(published_year=published_year)

    books = Book.objects.filter(query).order_by('-published_year', 'title')

    paginator = Paginator(books, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/shop.html', {
        'books': page_obj,  
        'form': form,
        'liked_books': liked_books,
    })


# Book Actions
@login_required(login_url='login')
def like_book(request, id):
    book = get_object_or_404(Book, id=id)
    like, created = Like.objects.get_or_create(user=request.user, book=book)

    if not created:
        like.delete()
        messages.info(request, f'You unliked "{book.title}"')
    else:
        messages.success(request, f'You liked "{book.title}"')

    return redirect('books')


def details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'core/details.html', {'book': book})


@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)

        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.author = request.user
            book.save()
            messages.success(request, "Book added successfully!")
            return redirect('books')

        messages.error(request, "There were errors in the form. Please check and try again.")

    else:
        book_form = BookForm()

    return render(request, 'core/add_book.html', {'form': book_form})


@login_required(login_url='login')
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    
    if request.method == 'POST':
        if book.author != request.user:
            messages.error(request, 'You can\'t delete this book.')
        else:
            book.delete()
            messages.success(request, f'"{book.title}" was successfully deleted.')

    return redirect('books')


@login_required(login_url='login')
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    if request.user != book.author:
        messages.error(request, "You don't have permission to edit this book")
        return redirect('home')

    form = BookForm(request.POST or None, request.FILES or None, instance=book)

    if request.method == 'POST' and form.is_valid():
        book = form.save()
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('books')

    return render(request, 'core/edit_book.html', {'form': form, 'book': book})


@login_required(login_url='login')
def add_genre(request):
    form = GenreForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Genre added successfully!')
        return redirect('books')

    return render(request, 'core/add_genre.html', {'form': form})

def my_profile(request, id):
    user_profile = get_object_or_404(User, id=id)
    
    authored_books = Book.objects.filter(author=user_profile)
    liked_books = Like.objects.filter(user=user_profile).select_related('book')

    context = {
        'user_profile': user_profile,
        'authored_books': authored_books,
        'liked_books': liked_books,
    }
    
    return render(request, 'core/my_profile.html', context)
