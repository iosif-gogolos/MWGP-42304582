from django.contrib import admin

from .models import (
    WG, MitbewohnerProfil, Raum, Reinigungsaufgabe, 
    Putzplan, Kalendereintrag, AufgabenStatus
)

# Register your models here.

admin.site.register(WG)
admin.site.register(MitbewohnerProfil)
admin.site.register(Raum)
admin.site.register(Reinigungsaufgabe)
admin.site.register(Putzplan)
admin.site.register(AufgabenStatus)
admin.site.register(Kalendereintrag)


