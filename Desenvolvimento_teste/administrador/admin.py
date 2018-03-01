from django.contrib import admin
from .models import Controle_Arrecadacao, Controle_Usuario
from administrador.models import Controle_Embarcacao, Controle_Despesas,\
    Controle_Anual

class EmbarcacaoAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'nome',
                    'proprietario',
                    ]
    
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'user',
                    'nome',
                    'cargo',
                    'barco',
                    ]
    
class ArrecadacaoAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'barco',
                    'data_viagem',
                    'qnt_passagem',
                    'qnt_adulto',
                    'qnt_crianca',
                    'alimentacao',
                    'encomendas',
                    'total',]

class DespesasAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'barco',
                    'data_viagem',
                    'qnt_combustivel',
                    'preco_combustivel',
                    'total',
                    'tripulacao',
                    'alimentacao',
                    'outros',
                    'total',]

class ControleAnualAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'barco',
                    'mes',
                    'receita_total',
                    'despesa_total',]

    
admin.site.register(Controle_Embarcacao, EmbarcacaoAdmin)
admin.site.register(Controle_Usuario, UsuarioAdmin)
admin.site.register(Controle_Arrecadacao, ArrecadacaoAdmin)
admin.site.register(Controle_Despesas, DespesasAdmin)
admin.site.register(Controle_Anual, ControleAnualAdmin)

