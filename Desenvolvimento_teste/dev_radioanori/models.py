from django.conf import settings
from django.db import models
from administrador.models import Controle_Embarcacao
from django.forms.models import ModelForm
from .managers import CartManager, PurchaseManager

from pagseguro.signals import notificacao_recebida
from _datetime import date, datetime
from django.template.defaultfilters import default


class Viagem(models.Model):
    CIDADES_CHOICES = (
        ('Anori', 'Anori'),
        ('Anama', 'Anama'),
        ('Codajas', 'Codajas'),
        ('Coari', 'Coari'),
        ('Manaus', 'Manaus'),
        ('Manacapuru', 'Manaucapuru'),
    )
    origem = models.CharField(max_length=10, choices=CIDADES_CHOICES, default='Manaus')
    destino = models.CharField(max_length=10, choices=CIDADES_CHOICES, default='Anori')
    embarcacao = models.ForeignKey(Controle_Embarcacao)
    preco_adulto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    preco_crianca = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    data_da_viagem = models.DateField(null=True, blank=True)
    porto = models.CharField(max_length=20)
    foto_embarcacao = models.ImageField()
    
    
class Compra(models.Model):
    viagem = models.ForeignKey(Viagem, null=True, blank=True)
    qnt_adulto = models.IntegerField(null=False, blank=False, default=1)
    qnt_crianca = models.IntegerField(blank=True, default=0)
    nome_passageiro = models.CharField(max_length=20)

class Carrinho(models.Model):
    viagem = models.ForeignKey(Viagem, null=True, blank=True)
    qnt_inteira = models.IntegerField(null=True, blank=True, default=1)
    qnt_meia = models.PositiveIntegerField(default=0)
    total = models.FloatField(null=True, blank=True)
    
    
class Passagem(models.Model):
    poltrona = models.CharField(max_length=3, null=True, blank=True)
    carrinho = models.ForeignKey(Carrinho)
    nome_passageiro = models.CharField(max_length=200)
    cpf = models.IntegerField(null=True, blank=True)
     

class Venda(models.Model):
    data_venda = models.DateField(blank=True, null=False)
    qnt_passagem = models.IntegerField(blank=True, null=False)
    Passagem = models.ForeignKey(Passagem)
    total = models.FloatField(blank=True, null=False) 
    
    def __str__(self):
        return self.pk  


class Poltrona(models.Model):
    viagem = models.ForeignKey(Viagem)
    poltronas_indisponiveis = models.CharField(max_length=500, null=True, blank=True)
    criacao = models.DateTimeField(auto_now_add =True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)



#===============================================================================
# class BaseModel(models.Model):
#     
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# 
#     class Meta:
#         abstract = True
# 
# class Ticket(BaseModel):
#     viagem = models.ForeignKey('Viagem', on_delete=models.CASCADE, verbose_name='viagem', related_name='tickets')
#     title = models.CharField('título', max_length=128)
#     type = models.SmallIntegerField('type', default=1)
#     price = models.DecimalField('preço', max_digits=10, decimal_places=2)
# 
# 
#     class Meta:
#         ordering = ['title']
#         verbose_name = 'ticket'
#         verbose_name_plural = 'tickets'
# 
# 
# class Cart(BaseModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='usuário', related_name='carts')
#     closed = models.BooleanField('carrinho finalizado', db_index=True, default=False)
#     objects = CartManager()
# 
#     
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = 'carrinho de compra'
#         verbose_name_plural = 'carrinhos de compra'
# 
#     @property
#     def price(self):
#         return sum([cart_item.price for cart_item in self.cart_items.all()])
# 
# 
# class CartItem(BaseModel):
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='carrinho', related_name='cart_items')
#     ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, verbose_name='ticket', related_name='cart_items')
#     quantity = models.SmallIntegerField('quantidade', default=1)
#     unit_price = models.DecimalField('preço unitário', max_digits=10, decimal_places=2)
# 
#     
#     class Meta:
#         ordering = ['id']
#         verbose_name = 'item do carrinho de compra'
#         verbose_name_plural = 'itens do carrinho de compra'
#         unique_together = ('cart', 'ticket')
# 
#     @property
#     def price(self):
#         return self.quantity * self.unit_price
# 
# 
# PURCHASE_STATUS_CHOICES = (
#     ('pending', 'Pendente'),
#     ('paid', 'Pago'),
#     ('canceled', 'Cancelado'),
# )
# 
# 
# class Purchase(BaseModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='usuário', related_name='purchases')
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='carrinho', related_name='purchases')
#     price = models.DecimalField('preço', max_digits=10, decimal_places=2)
#     status = models.CharField('status da compra', max_length=16, default='pending', choices=PURCHASE_STATUS_CHOICES)
#     pagseguro_redirect_url = models.URLField('url do pagseguro', max_length=255, blank=True)
#     objects = PurchaseManager()
# 
#     def __str__(self):
#         return str(self.id)
# 
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = 'compra'
#         verbose_name_plural = 'compras'
# 
# 
# def update_purchase_status(sender, transaction, **kwargs):
#     Purchase.objects.update_purchase_status(transaction)
# 
# 
# notificacao_recebida.connect(update_purchase_status)
#===============================================================================

#===============================================================================
# class CartItemForm(ModelForm):
#     class Meta: 
#         model = CartItem
#         exclude = ('cart','unit_price')
#===============================================================================
