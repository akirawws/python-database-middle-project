from django.contrib import admin
from .models import Author, Genre, Client, Book, BookLoan, Publisher, Review

# Register your models here.

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Client)
admin.site.register(Book)
admin.site.register(BookLoan)
admin.site.register(Publisher)
admin.site.register(Review)