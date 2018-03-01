from django.contrib import admin

from .models import Viagem, Compra, Carrinho

class ViagemAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'origem',
                    'destino',
                    'embarcacao',
                    'preco_adulto',
                    'preco_crianca',
                    'data_da_viagem',]

admin.site.register(Viagem, ViagemAdmin)
admin.site.register(Compra)
admin.site.register(Carrinho)
