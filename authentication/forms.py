from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm):
    """
    A form for user registration that extends Django's UserCreationForm.

    This form adds email, first name, and last name fields to the default
    username and password fields provided by UserCreationForm. All fields
    are styled using Bootstrap's 'form-control' class.
    """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

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

        This method is overridden to add Bootstrap's 'form-control' class
        to the widget of each form field for consistent styling across
        all fields, including those inherited from UserCreationForm.
        """
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})