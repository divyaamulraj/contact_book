from django.db import models

from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator

phone_validator = RegexValidator(
    regex=r"^\+?\d{10,15}$",
    message="Enter a valid phone number (10–15 digits, optional + prefix).",
)

class Contact(models.Model):
    name   = models.CharField(max_length=100)
    phone  = models.CharField(
        max_length=15,
        validators=[phone_validator],
        help_text="10–15 digits, optionally starting with +",
    )
    city   = models.CharField(max_length=80, blank=True)
    state  = models.CharField(max_length=80, blank=True)
    email  = models.EmailField(validators=[EmailValidator()])

    created_at = models.DateTimeField(auto_now_add=True)   # optional audit fields
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]          # newest first
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.name} ({self.phone})"

# Create your models here.
