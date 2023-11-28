from django.db import models
from django.contrib.postgres.fields import ArrayField


class Author(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    born_date = models.CharField(max_length=100, blank=True, null=True)
    born_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Quote(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    tags = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField(blank=False, null=False)
