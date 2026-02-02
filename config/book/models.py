from django.db import models
from author.models import Authors
# Create your models here.
class Book(models.Model):
    title= models.CharField(max_length=100)
    author = models.ForeignKey(Authors,on_delete=models.CASCADE,related_name="author")


    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
 