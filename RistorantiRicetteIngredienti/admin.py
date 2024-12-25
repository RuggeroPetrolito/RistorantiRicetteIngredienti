from django.contrib import admin

from .models import Ristorante, Ricetta, Ingrediente, RistoranteToRicetta, RicettaToIngrediente

class RistoranteToRicettaInline(admin.TabularInline):
    model = RistoranteToRicetta
    extra = 1

class RicettaToIngredienteInline(admin.TabularInline):
    model = RicettaToIngrediente
    extra = 1

class RistoranteAdmin(admin.ModelAdmin):
    inlines = (RistoranteToRicettaInline,)

class RicettaAdmin(admin.ModelAdmin):
    inlines = (RistoranteToRicettaInline, RicettaToIngredienteInline,)

class IngredienteAdmin(admin.ModelAdmin):
    inlines = (RicettaToIngredienteInline,)

admin.site.register(Ristorante, RistoranteAdmin)
admin.site.register(Ricetta, RicettaAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(RistoranteToRicetta)
admin.site.register(RicettaToIngrediente)