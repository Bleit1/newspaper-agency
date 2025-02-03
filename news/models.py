from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField("Name Topics", max_length=100)

    def __str__(self):
        return self.name

class NewspaperIssue(models.Model):
    title = models.CharField("Title of the news", max_length=200)
    content = models.TextField("Content of news")
    publication_date = models.DateField("Public date", auto_now_add=True)
    editors = models.ManyToManyField(User, verbose_name="Editors")
    topics = models.ManyToManyField(Topic, verbose_name="Topics", blank=True)

    def __str__(self):
        return self.title
