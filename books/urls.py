from django.urls import path
from books import views

urlpatterns = [
    path('external-books', views.ExternalBook.as_view()),
]
