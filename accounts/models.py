from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string

# Create your models here.
class Benutzer(AbstractUser):
    """
    Erweiterte Benutzerklasse mit benutzerdefinierten Attributen
    """
    
    ist_admin = models.BooleanField(
        default=False,
        verbose_name='Ist Admin',
        help_text='Aktivieren Sie dieses Feld, wenn der Benutzer Administratorrechte haben soll.'
    )
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Benutzer'
        verbose_name_plural = 'Benutzer'
        ordering = ['erstellt_am']
    
    def __str__(self):
        return f"{self.erstellt_am} Ein neuer Benutzer. Ist Admin? {self.ist_admin}"
    