from django.db import models
from django.utils import timezone
from accounts.models import Benutzer
from datetime import datetime, timedelta

# Create your models here.
class WG(models.Model):
    """
    Wohngemeinschaft
    """
    name = models.CharField(max_length=100)
    adresse = models.TextField()
    erstellt_am = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'WG'
        verbose_name_plural = 'WGs'
    
    def __str__(self):
        return self.name


class MitbewohnerProfil(models.Model):
    """
    Profil für Mitbewohner mit Bezug zur WG
    """
    benutzer = models.OneToOneField(
        Benutzer, 
        on_delete=models.CASCADE, 
        related_name='mitbewohner_profil'
    )
    wg = models.ForeignKey(
        WG, 
        on_delete=models.CASCADE, 
        related_name='mitbewohner'
    )
    beigetreten_am = models.DateTimeField(auto_now_add=True)
    ist_aktiv = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Mitbewohner Profil'
        verbose_name_plural = 'Mitbewohner Profile'
        unique_together = ['benutzer', 'wg']
    
    def __str__(self):
        return f"{self.benutzer} - {self.wg}"
    
    def kann_aufgaben_abhaken(self):
        """Mitbewohner können Aufgaben abhaken"""
        return True
    
    def kann_putztag_beenden(self):
        """Mitbewohner können Putztage als beendet markieren"""
        return True


class Raum(models.Model):
    """
    Gemeinsam genutzte Räume in der WG
    """
    wg = models.ForeignKey(
        WG, 
        on_delete=models.CASCADE, 
        related_name='raeume'
    )
    bezeichnung = models.CharField(max_length=50)
    beschreibung = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Raum'
        verbose_name_plural = 'Räume'
        unique_together = ['wg', 'bezeichnung']
    
    def __str__(self):
        return f"{self.bezeichnung} ({self.wg})"
    
class Reinigungsaufgabe(models.Model):
    """
    Reinigungsaufgaben für jeden Raum
    """
    raum = models.ForeignKey(
        Raum, 
        on_delete=models.CASCADE, 
        related_name='aufgaben'
    )
    bezeichnung = models.CharField(max_length=100)
    beschreibung = models.TextField(blank=True)
    haeufigkeit = models.IntegerField(
        default=1, 
        help_text="Wie oft pro Woche (Standard: 1 = wöchentlich)"
    )
    schaetzzeit_minuten = models.IntegerField(
        default=30,
        help_text="Geschätzte Zeit in Minuten"
    )
    
    class Meta:
        verbose_name = 'Reinigungsaufgabe'
        verbose_name_plural = 'Reinigungsaufgaben'
    
    def __str__(self):
        return f"{self.bezeichnung} - {self.raum}"
    
class Putzplan(models.Model):
    """
    Putzplan für eine WG
    """
    wg = models.OneToOneField(
        WG, 
        on_delete=models.CASCADE, 
        related_name='putzplan'
    )
    erstellungsdatum = models.DateTimeField(auto_now_add=True)
    ist_aktiv = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Putzplan'
        verbose_name_plural = 'Putzpläne'
    
    def __str__(self):
        return f"Putzplan - {self.wg}"
    
    def naechster_sonntag(self):
        """Berechnet den nächsten Sonntag"""
        heute = timezone.now().date()
        tage_bis_sonntag = (6 - heute.weekday()) % 7
        if tage_bis_sonntag == 0:  # Heute ist Sonntag
            tage_bis_sonntag = 7
        return heute + timedelta(days=tage_bis_sonntag)
    
    def aufgaben_umverteilen(self):
        """Verteilt Aufgaben auf die Mitbewohner um"""
        # Implementierung der Rotation Logic
        pass


class Kalendereintrag(models.Model):
    """
    Einzelner Eintrag im Putzkalender
    """
    STATUS_CHOICES = [
        ('done', 'Erledigt'),
        ('upcoming', 'Anstehend'),
        ('future', 'Zukünftig'),
        ('overdue', 'Überfällig'),
    ]
    
    putzplan = models.ForeignKey(
        Putzplan, 
        on_delete=models.CASCADE, 
        related_name='eintraege'
    )
    mitbewohner = models.ForeignKey(
        MitbewohnerProfil, 
        on_delete=models.CASCADE, 
        related_name='putztermine'
    )
    datum = models.DateField()
    aufgaben = models.ManyToManyField(
        Reinigungsaufgabe, 
        through='AufgabenStatus'
    )
    ist_beendet = models.BooleanField(default=False)
    beendet_am = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Kalendereintrag'
        verbose_name_plural = 'Kalendereinträge'
        unique_together = ['putzplan', 'datum']
        ordering = ['datum']
    
    def __str__(self):
        return f"{self.datum} - {self.mitbewohner}"
    
    @property
    def status(self):
        """Berechnet den Status basierend auf dem Datum"""
        heute = timezone.now().date()
        
        if self.ist_beendet:
            return 'done'
        elif self.datum < heute:
            return 'overdue'
        elif self.datum == heute or (self.datum - heute).days <= 7:
            return 'upcoming'
        else:
            return 'future'
    
    def eintrag_markieren_beendet(self):
        """Markiert den Putztag als beendet"""
        self.ist_beendet = True
        self.beendet_am = timezone.now()
        self.save()


class AufgabenStatus(models.Model):
    """
    Zwischenmodell für den Status einzelner Aufgaben
    """
    kalendereintrag = models.ForeignKey(
        Kalendereintrag, 
        on_delete=models.CASCADE
    )
    aufgabe = models.ForeignKey(
        Reinigungsaufgabe, 
        on_delete=models.CASCADE
    )
    ist_erledigt = models.BooleanField(default=False)
    erledigt_am = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Aufgaben Status'
        verbose_name_plural = 'Aufgaben Status'
        unique_together = ['kalendereintrag', 'aufgabe']
    
    def __str__(self):
        status = "✓" if self.ist_erledigt else "○"
        return f"{status} {self.aufgabe.bezeichnung}"
    
    def abhaken(self):
        """Hakt eine Aufgabe ab"""
        self.ist_erledigt = True
        self.erledigt_am = timezone.now()
        self.save()


# Zusätzliche Manager für erweiterte Queries
class KalendereintragManager(models.Manager):
    def upcoming(self):
        """Gibt anstehende Einträge zurück"""
        heute = timezone.now().date()
        return self.filter(
            datum__gte=heute,
            ist_beendet=False
        ).order_by('datum')
    
    def done(self):
        """Gibt erledigte Einträge zurück"""
        return self.filter(ist_beendet=True).order_by('-datum')
    
    def future(self):
        """Gibt zukünftige Einträge zurück"""
        heute = timezone.now().date()
        naechste_woche = heute + timedelta(days=7)
        return self.filter(datum__gt=naechste_woche).order_by('datum')

# Manager zu Kalendereintrag hinzufügen
Kalendereintrag.add_to_class('objects', KalendereintragManager())