

from django.urls import path

from rest_framework.routers import DefaultRouter


from books import views


urlpatterns = [
    path('external-books', views.ExternalBook.as_view(), name='external_books'),
]

router = DefaultRouter()

router.register(r'v1/books', views.BookViewSet)

urlpatterns += router.urls
