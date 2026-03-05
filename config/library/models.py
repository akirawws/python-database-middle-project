from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    title_genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title_genre
    
class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_available_prime = models.BooleanField(default=True)
    price = models.CharField(max_length=20, null=True)
    age_min = models.CharField(null=True)

    def __str__(self):
        return self.title 
    
class Client(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    prime_status = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    text = models.TextField()
    rate = models.IntegerField()

    def __str__(self):
        return f"{self.book} | {self.client} | оценка: {self.rate} "

class BookLoan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_taken = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.client} - {self.book}"
    
