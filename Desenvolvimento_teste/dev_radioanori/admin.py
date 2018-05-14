from django.contrib import admin

from .models import Viagem, Compra, Carrinho, Passagem, Poltrona
#from dev_radioanori.models import Ticket, CartItem, Cart

class ViagemAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'origem',
                    'destino',
                    'barco',
                    'preco_adulto',
                    'preco_crianca',
                    'data_da_viagem',]
    def barco(self, obj):
        return obj.embarcacao.nome
    

class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'barco',
                    'qnt_inteira',
                    'qnt_meia',
                    'total',]
    def barco(self, obj):
        return obj.viagem.embarcacao

class PassagemAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'poltrona',
                    'carrinho_pk',
                    'nome_passageiro',]
    
    def carrinho_pk(self, obj):
        return obj.carrinho.pk

class PoltronaAdmin(admin.ModelAdmin):
    list_display = ['pk',
                    'viagem_barco',
                    'poltronas_indisponiveis',
                    'ultima_atualizacao',]
    
    def viagem_barco(self, obj):
        return obj.viagem.embarcacao

    
#===============================================================================
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['pk',
#                     'user',
#                     'closed',
#                     'objects',
#                     ]
# 
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ['pk',
#                     'cart',
#                     'ticket',
#                     'quantity',
#                     'unit_price',]
#     
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ['pk',
#                     'viagem',
#                     'type',
#                     'price',
#                     ]
#===============================================================================
admin.site.register(Viagem, ViagemAdmin)
admin.site.register(Compra)
admin.site.register(Carrinho, CarrinhoAdmin)
admin.site.register(Passagem, PassagemAdmin)
admin.site.register(Poltrona, PoltronaAdmin)

#===============================================================================
# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)
# admin.site.register(Ticket, TicketAdmin)
#===============================================================================

