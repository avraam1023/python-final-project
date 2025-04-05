from django.urls import path
from . import views 

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Bookstore
    path('', views.home, name='home'),
    path('books/', views.shop, name='books'), 
    path('book/<int:id>/like/', views.like_book, name='like_book'),
    path('details/<int:pk>/', views.details, name='details'),

    # Book Management
    path('add_book/', views.add_book,  name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('my_profile/<int:id>', views.my_profile, name='my_profile')
    ]
