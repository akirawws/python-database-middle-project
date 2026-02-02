from django.db import models
from book.models import Book
# Create your models here.
class Library(models.Model):
    title_library = models.CharField(max_length=100)
    count_book = models.PositiveIntegerField(default=0)
    books = models.ExpressionList
    def count_books(self):
        self.count_book = len(Book.objects.all())