from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from .models import NewspaperIssue, Reaction
from .forms import NewspaperIssueForm, CommentForm, ReactionForm

def issue_list(request):
    issues = NewspaperIssue.objects.all().order_by('-publication_date')
    return render(request, 'news/issue_list.html', {'issues': issues})

def main(request):
    query = request.GET.get('q', '')
    if query:
        news_list = NewspaperIssue.objects.filter(title__icontains=query).order_by('-publication_date')
    else:
        news_list = NewspaperIssue.objects.order_by('-publication_date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'query': query}
    return render(request, 'news/main.html', context)

def latest(request):
    latest_news = NewspaperIssue.objects.order_by('-publication_date')
    context = {'latest_news': latest_news}
    return render(request, 'news/latest.html', context)


def issue_detail(request, pk):
    issue = get_object_or_404(NewspaperIssue, pk=pk)
    comments = issue.comments.order_by('-created_at')
    comment_form = CommentForm()
    likes = issue.reactions.filter(reaction='like').count()
    dislikes = issue.reactions.filter(reaction='dislike').count()
    context = {
        'issue': issue,
        'comments': comments,
        'comment_form': comment_form,
        'likes': likes,
        'dislikes': dislikes,
    }
    return render(request, 'news/issue_detail.html', context)

def create_news(request):
    if request.method == 'POST':
        form = NewspaperIssueForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            form.save_m2m()
            return redirect('issue_list')
    else:
        form = NewspaperIssueForm()
    return render(request, 'news/create_news.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('issue_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

def custom_logout(request):
    if not request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        logout(request)
        return redirect('main')
    return render(request, 'registration/logout.html')

@require_POST
def add_comment(request, pk):
    issue = get_object_or_404(NewspaperIssue, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        if request.user.is_authenticated:
            comment.author = request.user.username
        comment.issue = issue
        comment.save()
    return redirect('issue_detail', pk=pk)

@require_POST
def add_reaction(request, pk):
    issue = get_object_or_404(NewspaperIssue, pk=pk)
    user = request.user if request.user.is_authenticated else None
    ip = request.META.get('REMOTE_ADDR')
    form = ReactionForm(request.POST)
    if form.is_valid():
        reaction_value = form.cleaned_data['reaction']
        try:
            if user:
                existing = Reaction.objects.get(issue=issue, user=user)
            else:
                existing = Reaction.objects.get(issue=issue, ip_address=ip)
            if existing.reaction == reaction_value:
                existing.delete()
            else:
                existing.reaction = reaction_value
                existing.save()
        except Reaction.DoesNotExist:
            Reaction.objects.create(issue=issue, user=user, ip_address=ip, reaction=reaction_value)
    return redirect('issue_detail', pk=pk)


@require_POST
def custom_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main')
    else:
        context = {'error': 'Invalid username or password'}
        return render(request, 'registration/login.html', context)