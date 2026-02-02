from django.db import models


class Authors(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


    # def count_books(self):
    #      count_book=0
    #      books = Book.objects.all()
    #      for book in books:
             
