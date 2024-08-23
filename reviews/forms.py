from django import forms
from .models import Review, Ticket

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]  
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Note'
    )
    headline = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre de la critique'
        }),
        label='Titre de la critique'
    )
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'comment'] 
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Commentaire',
                'rows': 5
            })
        }
        labels = {
            'comment': 'Commentaire'
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre/article'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 5
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image'
        }