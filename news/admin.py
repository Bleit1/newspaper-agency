from django.contrib import admin
from .models import NewspaperIssue, Topic

class NewspaperIssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'featured')
    list_filter = ('featured', 'publication_date', 'topics')
    search_fields = ('title', 'content')
    filter_horizontal = ('editors', 'topics')

admin.site.register(NewspaperIssue, NewspaperIssueAdmin)
admin.site.register(Topic)
