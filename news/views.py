from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required

from news.models import NewspaperIssue, Reaction, Topic
from news.forms import NewspaperIssueForm, CommentForm, ReactionForm


def issue_list(request):
    topics = Topic.objects.all()
    selected_topics = request.GET.getlist('topics')

    news = NewspaperIssue.objects.all()
    if selected_topics:
        news = news.filter(topics__id__in=selected_topics).distinct()

    return render(request, 'news/issue_list.html', {
        'topics': topics,
        'news': news,
    })


def main(request):
    query = request.GET.get('q', '')
    news_list = NewspaperIssue.objects.order_by('-publication_date')
    if query:
        news_list = news_list.filter(title__icontains=query)

    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'news/main.html', context)


def latest(request):
    try:
        limit = int(request.GET.get('limit', 6))
    except ValueError:
        limit = 6

    query = request.GET.get('q', '')
    news_list = NewspaperIssue.objects.order_by('-publication_date')
    if query:
        news_list = news_list.filter(title__icontains=query)

    total_news = news_list.count()
    latest_news = news_list[:limit]

    context = {
        'latest_news': latest_news,
        'limit': limit,
        'total_news': total_news,
        'query': query,
    }
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


@permission_required('news.add_newspaperissue', login_url='login')
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


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html')


def custom_logout(request):
    logout(request)
    return redirect('main')
