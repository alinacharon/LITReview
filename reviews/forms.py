from django import forms
from .models import Review, Ticket

class BaseForm(forms.ModelForm):
    """Base form for all forms."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.FileInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': 'form-check-input'})

class ReviewForm(BaseForm):
    """For review creation and editing."""

    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label='Note'
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'comment']
        labels = {
            'headline': 'Titre de la critique',
            'comment': 'Commentaire'
        }
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Titre de la critique'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Commentaire', 'rows': 5})
        }

class TicketForm(BaseForm):
    """For ticket creation and editing."""

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du livre/article'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 5}),
            'image': forms.ClearableFileInput()
        }
