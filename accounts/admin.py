from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Materiel)

admin.site.register(Employee)

admin.site.register(Etablissement)

admin.site.register(Emplacement)

admin.site.register(Affectation)