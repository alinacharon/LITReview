from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    """
    Validator to check if the password contains at least one letter.
    """

    def validate(self, password, user=None):
        """
        Checks if the password contains at least one letter.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object, if applicable.

        Raises:
            ValidationError: If the password doesn't contain any letters.
        """
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')

    def get_help_text(self):
        """
        Returns the help text for this validator.

        Returns:
            str: The help text.
        """
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'


class ContainsNumberValidator:
    """
    Validator to check if the password contains at least one number.
    """

    def validate(self, password, user=None):
        """
        Checks if the password contains at least one number.

        Args:
            password (str): The password to validate.
            user (User, optional): The user object, if applicable.

        Raises:
            ValidationError: If the password doesn't contain any numbers.
        """
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir un chiffre', code='password_no_number')

    def get_help_text(self):
        """
        Returns the help text for this validator.

        Returns:
            str: The help text.
        """
        return 'Votre mot de passe doit contenir au moins un chiffre.'
