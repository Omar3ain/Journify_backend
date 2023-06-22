import re
from django.core.exceptions import ValidationError

class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[a-z]', password):
            raise ValidationError(
                "The password must contain at least 1 lowercase character.",
                code='password_no_lowercase',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 lowercase character."

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                "The password must contain at least 1 uppercase character.",
                code='password_no_uppercase',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase character."

class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "The password must contain at least 1 special character: " +
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 special character: " \
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"