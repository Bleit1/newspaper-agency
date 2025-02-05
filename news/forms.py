from django import forms
from .models import NewspaperIssue, Comment, Reaction

class NewspaperIssueForm(forms.ModelForm):
    class Meta:
        model = NewspaperIssue
        fields = ['title', 'content', 'editors', 'topics', 'photo']
        widgets = {
            'topics': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your comment...'}),
        }

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['reaction']
        widgets = {
            'reaction': forms.RadioSelect(choices=Reaction._meta.get_field('reaction').choices)
        }
