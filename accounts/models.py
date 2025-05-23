from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string

# Create your models here.
class Benutzer(AbstractUser):
    """
    Erweiterte Benutzerklasse mit benutzerdefinierten Attributen
    """
    vorname = models.CharField(max_length=50, verbose_name='Vorname')
    nachname = models.CharField(max_length=50, verbose_name='Nachname')
    email = models.EmailField(unique=True, verbose_name='E-Mail')
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
        return f"{self.vorname} {self.nachname}"
    
    def passwort_generieren(self):
        """
        Generiert ein zufälliges Passwort mit einer Länge von 8 Zeichen.
        """
        passwort =  string.ascii_letters + string.digits
        return ''.join(secrets.choice(passwort) for _ in range(8))