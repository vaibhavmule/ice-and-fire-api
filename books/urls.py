

from django.urls import path

from rest_framework.routers import DefaultRouter


from books import views


urlpatterns = [
    path('', views.api_root),
    path('external-books', views.ExternalBook.as_view(), name='external_books'),
]

router = DefaultRouter(trailing_slash=False)

router.register(r'v1/books', views.BookViewSet, base_name='books')

urlpatterns += router.urls
