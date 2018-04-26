from django.db import models
from administrador.models import Controle_Embarcacao

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
    embarcacao = models.CharField(max_length=20)
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
    qnt_meia = models.IntegerField(null=True, blank=True, default=0)
    total = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.pk.__str__()
    
class Passagem(models.Model):
    poltrona = models.CharField(max_length=3, null=True, blank=True)
    carrinho = models.ForeignKey(Carrinho)
    nome_passageiro = models.CharField(max_length=20)
     
    def __str__(self):
        return self.pk.__str__()

class Venda(models.Model):
    data_venda = models.DateField(blank=True, null=False)
    qnt_passagem = models.IntegerField(blank=True, null=False)
    Passagem = models.ForeignKey(Passagem)
    total = models.FloatField(blank=True, null=False) 
    
    def __str__(self):
        return self.pk  