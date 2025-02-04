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
    photo = models.ImageField("Image", upload_to='news_photos/', blank=True, null=True)
    featured = models.BooleanField("Featured", default=False)
    def __str__(self):
        return self.title

class Comment(models.Model):
    issue = models.ForeignKey('NewspaperIssue', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField("Comment")
    author = models.CharField("Author", max_length=100, default="Anonymous")
    created_at = models.DateTimeField("Create Date", auto_now_add=True)
    def __str__(self):
        return f"{self.author}: {self.content[:30]}..."

REACTION_CHOICES = (
    ('like', 'Like'),
    ('dislike', 'Dislike'),
)

class Reaction(models.Model):
    issue = models.ForeignKey('NewspaperIssue', related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    reaction = models.CharField("Reaction", max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [
            ('issue', 'user'),
            ('issue', 'ip_address'),
        ]
    def __str__(self):
        return f"{self.reaction} for {self.issue.title}"
