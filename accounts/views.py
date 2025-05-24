from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Benutzer
from reinigung.models import WG, MitbewohnerProfil
import secrets
import string

def login_view(request):
    """
    Benutzeranmeldung
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Ungültige Anmeldedaten')
    
    return render(request, 'accounts/login.html')

@login_required
def create_user(request):
    """
    Neuen Mitbewohner erstellen (nur für Admins)
    """
    if not request.user.ist_admin:
        messages.error(request, 'Keine Berechtigung')
        return redirect('dashboard')
    
    if request.method == 'POST':
        vorname = request.POST.get('vorname')
        nachname = request.POST.get('nachname')
        email = request.POST.get('email')
        
        # Prüfen ob E-Mail bereits existiert
        if Benutzer.objects.filter(email=email).exists():
            messages.error(request, 'E-Mail-Adresse bereits vergeben')
            return render(request, 'accounts/create_user.html')
        
        # Zufälliges Passwort generieren
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        passwort = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        # Benutzer erstellen
        user = Benutzer.objects.create_user(
            username=email,
            email=email,
            vorname=vorname,
            nachname=nachname,
            password=passwort
        )
        
        # Mitbewohner-Profil erstellen
        try:
            wg = request.user.mitbewohner_profil.wg
            MitbewohnerProfil.objects.create(benutzer=user, wg=wg)
        except:
            # Fallback: Erste WG verwenden
            wg = WG.objects.first()
            if wg:
                MitbewohnerProfil.objects.create(benutzer=user, wg=wg)
        
        # E-Mail mit Login-Daten senden
        try:
            send_mail(
                subject='Willkommen bei MWGP - Ihre Login-Daten',
                message=f'''
Hallo {vorname},

Sie wurden als neuer Mitbewohner zu MWGP hinzugefügt.

Ihre Login-Daten:
E-Mail: {email}
Passwort: {passwort}

Loggen Sie sich unter http://localhost:8000 ein.

Viele Grüße,
Ihr MWGP-Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f'Mitbewohner {vorname} {nachname} erfolgreich erstellt und E-Mail versendet!')
        except Exception as e:
            messages.warning(request, f'Mitbewohner erstellt, aber E-Mail konnte nicht versendet werden: {str(e)}')
        
        return redirect('dashboard')
    
    return render(request, 'accounts/create_user.html')

