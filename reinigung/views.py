from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import (
    WG, MitbewohnerProfil, Raum, Reinigungsaufgabe, 
    Putzplan, Kalendereintrag, AufgabenStatus
)
from accounts.models import Benutzer

def landing_page(request):
    """
    Öffentliche Langing-Page für MWGP
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'reinigung/landing.html')

@login_required #Dekorator für Authentifizierung
def dashboard(request):
    """
    Hauptansicht - Kalenderübersicht mit Putzplan
    """
    
    # Ermittlung der WG des Benutzers unter Fehlerbehandlung
    wg = None
    putzplan = None
    try:
        mitbewohner_profil = request.user.mitbewohner_profil
        wg = mitbewohner_profil.wg
        putzplan = wg.putzplan
    except:
        # Falls noch keine WG existiert, Dummy-Daten verwenden
        if not wg:
            wg = WG.objects.create(name="Meine WG", adresse="WG Adresse")
            messages.info(request, "Eine Standard-WG wurde erstellt.")
    
    # Kalender-Daten für die nächsten 5 Sonntage (2 vergangen, 1 aktuell, 2 zukünftig)
    heute = timezone.now().date()
    
    # Berechnung der Sonntage
    sonntage = []
    aktueller_sonntag = heute - timedelta(days=heute.weekday() + 1) # Letzter Sonntag
    
    for i in range(-2, 3):  # -2 bis +2 Wochen
        sonntag = aktueller_sonntag + timedelta(weeks=i)
        
        # Status bestimmen
        if sonntag < heute:
            status = 'past'
        elif sonntag <= heute + timedelta(days=7):
            status = 'upcoming'
        else:
            status = 'future'
        
        # Kalendereintrag für diesen Sonntag suchen
        try:
            eintrag = Kalendereintrag.objects.get(
                putzplan=putzplan, 
                datum=sonntag
            ) if putzplan else None
            mitbewohner_name = eintrag.mitbewohner.benutzer.vorname if eintrag else "Unbekannt"
            ist_erledigt = eintrag.ist_beendet if eintrag else False
        except Kalendereintrag.DoesNotExist:
            # Dummy-Daten für Demo
            dummy_namen = ['Thorsten', 'Max', 'Lisa']
            mitbewohner_name = dummy_namen[i % len(dummy_namen)]
            ist_erledigt = status == 'past'
            eintrag = None
        
        sonntage.append({
            'datum': sonntag,
            'mitbewohner': mitbewohner_name,
            'status': status,
            'ist_erledigt': ist_erledigt,
            'eintrag': eintrag
        })
    
    # Reinigungsaufgaben für den aktuellen Benutzer
    aufgaben_nach_raum = {}
    if putzplan:
        # Aktuelle Aufgaben des Benutzers
        try:
            aktueller_eintrag = Kalendereintrag.objects.filter(
                putzplan=putzplan,
                mitbewohner__benutzer=request.user,
                datum__gte=heute,
                ist_beendet=False
            ).first()
            
            if aktueller_eintrag:
                aufgaben_status = AufgabenStatus.objects.filter(
                    kalendereintrag=aktueller_eintrag
                ).select_related('aufgabe__raum')
                
                for status in aufgaben_status:
                    raum_name = status.aufgabe.raum.bezeichnung
                    if raum_name not in aufgaben_nach_raum:
                        aufgaben_nach_raum[raum_name] = []
                    aufgaben_nach_raum[raum_name].append({
                        'id': status.pk,  # Primärschlüssel für AJAX-Updates
                        'bezeichnung': status.aufgabe.bezeichnung,
                        'ist_erledigt': status.ist_erledigt
                    })
        except:
            pass
    
    # Fallback: Dummy-Aufgaben wenn keine echten Daten vorhanden
    if not aufgaben_nach_raum:
        aufgaben_nach_raum = {
            'Küche': [
                {'id': 1, 'bezeichnung': 'Arbeitsflächen abwischen', 'ist_erledigt': False},
                {'id': 2, 'bezeichnung': 'Staubsaugen', 'ist_erledigt': False},
                {'id': 3, 'bezeichnung': 'Müll rausbringen', 'ist_erledigt': False},
                {'id': 4, 'bezeichnung': 'Putzen', 'ist_erledigt': False},
            ],
            'Bad': [
                {'id': 5, 'bezeichnung': 'Waschbecken und Toilette putzen', 'ist_erledigt': False},
                {'id': 6, 'bezeichnung': 'Müll entsorgen (Wenn voll ist)', 'ist_erledigt': False},
            ],
            'Flur': [
                {'id': 7, 'bezeichnung': 'Staubsaugen', 'ist_erledigt': False},
                {'id': 8, 'bezeichnung': 'Putzen', 'ist_erledigt': False},
            ]
        }
    
    # Admin-Willkommensnachricht prüfen
    zeige_admin_modal = request.user.ist_admin and not request.session.get('admin_welcome_shown', False)
    
    context = {
        'sonntage': sonntage,
        'aufgaben_nach_raum': aufgaben_nach_raum,
        'ist_admin': request.user.ist_admin,
        'zeige_admin_modal': zeige_admin_modal,
        'benutzer_name': f"{request.user.vorname} {request.user.nachname}",
        'wg': wg
    }
    
    return render(request, 'reinigung/dashboard.html', context)

@login_required
def aufgabe_abhaken(request):
    """
    AJAX-View zum Abhaken einer Aufgabe
    """
    if request.method == 'POST':
        aufgaben_id = request.POST.get('aufgaben_id')
        ist_erledigt = request.POST.get('ist_erledigt') == 'true'
        
        try:
            aufgaben_status = AufgabenStatus.objects.get(id=aufgaben_id)
            
            # Prüfen ob der Benutzer berechtigt ist
            if aufgaben_status.kalendereintrag.mitbewohner.benutzer == request.user:
                aufgaben_status.ist_erledigt = ist_erledigt
                if ist_erledigt:
                    aufgaben_status.erledigt_am = timezone.now()
                else:
                    aufgaben_status.erledigt_am = None
                aufgaben_status.save()
                
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Nicht berechtigt'})
                
        except AufgabenStatus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Aufgabe nicht gefunden'})
    
    return JsonResponse({'success': False, 'error': 'Ungültige Anfrage'})

@login_required
def putztag_beenden(request):
    """
    View zum Beenden eines Putztages
    """
    if request.method == 'POST':
        try:
            mitbewohner_profil = request.user.mitbewohner_profil
            
            # Aktuellen Kalendereintrag finden
            heute = timezone.now().date()
            kalendereintrag = Kalendereintrag.objects.filter(
                mitbewohner=mitbewohner_profil,
                datum__gte=heute,
                ist_beendet=False
            ).first()
            
            if kalendereintrag:
                kalendereintrag.eintrag_markieren_beendet()
                messages.success(request, 'Putztag erfolgreich als beendet markiert!')
            else:
                messages.error(request, 'Kein aktiver Putztag gefunden.')
                
        except Exception as e:
            messages.error(request, f'Fehler beim Beenden des Putztages: {str(e)}')
    
    return redirect('dashboard')

@login_required
def admin_welcome_dismiss(request):
    """
    Schließt das Admin-Willkommensdialog
    """
    request.session['admin_welcome_shown'] = True
    return JsonResponse({'success': True})