from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription étendant UserCreationForm de Django.
    Ajoute les champs email, prénom et nom, tous stylisés avec Bootstrap.
    """

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        """
        Meta class to specify the model and fields for the form.

        It uses the custom User model and includes all the necessary fields
        for user registration.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add 'form-control' class to form fields.
        
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})