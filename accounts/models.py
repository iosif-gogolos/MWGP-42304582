from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string

# Create your models here.
class Benutzer(AbstractUser):
    """
    Erweiterte Benutzerklasse mit benutzerdefinierten Attributen (Vererbung)
    """
    vorname = models.CharField(max_length=150, blank=True)
    nachname = models.CharField(max_length=150, blank=True)
    erst_anmeldung = models.BooleanField(default=False)
    
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
    
    def save(self, *args, **kwargs):
        # Mapping von Django's default Feldern zu den deutschen Feldnamen
        if not self.vorname and self.first_name:
            self.vorname = self.first_name
        if not self.nachname and self.last_name:
            self.nachname = self.last_name
        super().save(*args, **kwargs)
    