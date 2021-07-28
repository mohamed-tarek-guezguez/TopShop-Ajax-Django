from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Product(models.Model):
    Title = models.CharField(max_length=200)
    Slug = AutoSlugField(populate_from='Title', unique=True)
    Price = models.FloatField()
    Description = RichTextField(blank=True, null=True)
    Img = models.ImageField(upload_to='pics')
    Stock = models.IntegerField(default=0)
    CreatedAt = models.DateTimeField(default=timezone.now)

    number_of_reviews = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    totalRating = models.FloatField(default=0)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        self.number_of_reviews = Review.objects.filter(post_connected=self).count()
        if Review.objects.filter(post_connected=self).aggregate(Sum('rating'))['rating__sum'] != None:
            self.ratings = Review.objects.filter(post_connected=self).aggregate(Sum('rating'))['rating__sum']
        self.totalRating = 0
        if self.ratings != 0 and self.number_of_reviews != 0:
            self.totalRating = (self.ratings / self.number_of_reviews) * 20
        super().save(*args, **kwargs)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post_connected = models.ForeignKey(Product, on_delete=models.CASCADE)
