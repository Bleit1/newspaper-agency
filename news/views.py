from django.shortcuts import render, get_object_or_404
from .models import NewspaperIssue

def issue_list(request):
    issues = NewspaperIssue.objects.all().order_by('-publication_date')
    return render(request, 'news/issue_list.html', {'issues': issues})

def issue_detail(request, pk):
    issue = get_object_or_404(NewspaperIssue, pk=pk)
    return render(request, 'news/issue_detail.html', {'issue': issue})
