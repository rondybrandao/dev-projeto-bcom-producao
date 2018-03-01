from django.db import models

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
    preco_adulto = models.FloatField(null=True, blank=True)
    preco_crianca = models.FloatField(null=True, blank=True)
    data_da_viagem = models.DateField(null=True, blank=True)
    porto = models.CharField(max_length=20)
    foto_embarcacao = models.ImageField()
    
    
class Compra(models.Model):
    viagem = models.ForeignKey(Viagem, null=True, blank=True)
    qnt_adulto = models.IntegerField(null=False, blank=False, default=1)
    qnt_crianca = models.IntegerField(blank=True, default=0)
    nome_passageiro = models.CharField(max_length=20)

class Carrinho(models.Model):
    compra = models.ForeignKey(Compra)
    total = models.FloatField(null=True, blank=True)