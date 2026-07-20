import re
from django.core.exceptions import ValidationError


class LetterAndSymbolValidator:
    letter_re = re.compile(r"[A-Za-z]")
    symbol_re = re.compile(r"[^A-Za-z0-9]")

    def validate(self, password, user=None):
        if not self.letter_re.search(password):
            raise ValidationError(
                "Parolda kamida bitta harf bo'lishi kerak.",
                code="password_no_letter",
            )
        if not self.symbol_re.search(password):
            raise ValidationError(
                "Parolda kamida bitta maxsus belgi bo'lishi kerak.",
                code="password_no_symbol",
            )

    def get_help_text(self):
        return "Parolda kamida bitta harf va bitta maxsus belgi bo'lishi kerak."