from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Tag(models.Model):
     caption = models.CharField(max_length=20)
     
     def __str__(self):
          return f'{self.caption}'
     


class Author(models.Model):
     first_name = models.CharField(max_length=20)
     last_name = models.CharField(max_length=20)
     email_addr = models.EmailField()

     def author_detail(self):
          return f'{self.first_name} {self.last_name}'

     def __str__(self):
         return self.author_detail()



class Post(models.Model):
     title = models.CharField(max_length=50)
     excerpt = models.CharField(max_length=100)
     image_name = models.ImageField(upload_to="post")
     date = models.DateField(auto_now=True)
     slug = models.SlugField(unique=True, null=True)
     content = models.TextField(
          validators=[MinLengthValidator(10)])

     author = models.ForeignKey(
          Author, on_delete=models.SET_NULL, null=True, related_name="posts")

     tags = models.ManyToManyField(Tag)

     def __str__(self):
         return f'{self.title}'
     


class Comment(models.Model):
     user_name = models.CharField(max_length=20)
     user_email = models.EmailField()
     text = models.TextField(max_length=300)
     post = models.ForeignKey(
          Post, on_delete=models.CASCADE, related_name="comments")

     

