from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.widgets import Textarea


class Controle_Embarcacao(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    nome = models.CharField(max_length=20)
    proprietario = models.CharField(max_length=20)
    preco_passagem_inteira = models.FloatField(null=True, blank=True)
    preco_passagem_meia = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Controle_Usuario(models.Model):
    user = models.OneToOneField(User)
    nome = models.CharField(max_length=25)
    cargo = models.CharField(max_length=15)
    barco = models.ForeignKey(Controle_Embarcacao)
    
    def __str__(self):
        return self.nome
        
class Controle_Arrecadacao(models.Model):
    #user = models.ForeignKey(User)
    barco = models.ForeignKey(Controle_Embarcacao, null=True, blank=True)
    data_viagem = models.DateField(null=True, blank=True)      
    qnt_passagem = models.IntegerField(blank=True, default=0)
    qnt_adulto = models.IntegerField(blank=True, default=0)
    qnt_crianca = models.IntegerField(blank=True, default=0)
    alimentacao = models.FloatField(null=True, blank=True)
    encomendas = models.FloatField(blank=True)
    
    outros = models.FloatField(null=True, blank=True)   
    total = models.FloatField(blank=True, unique_for_date='data_viagem')
    
    class Meta:
        unique_together = ('data_viagem',)
        
    def __str__(self):
        return self.barco.__str__()
    
class Controle_Despesas(models.Model):
    
    barco = models.ForeignKey(Controle_Embarcacao, null=True, blank=True)
    data_viagem = models.DateField(null=True, blank=True)
    qnt_combustivel = models.FloatField(null=True, blank=True)
    preco_combustivel = models.FloatField(blank=True, default=0)
    total_combustivel = models.FloatField(blank=True, default=0)
    tripulacao = models.FloatField(null=False, blank=True, default=0)
    alimentacao = models.FloatField(blank=True, default=0)
    outros = models.FloatField(null=False, blank=True, default=0)   
    total = models.FloatField(blank=True, unique_for_date='data_viagem')
    
    class Meta:
        unique_together = ('data_viagem',)
    

   
class Controle_Anual(models.Model):
    JANEIRO = 'JAN'
    FEVEREIRO = 'FEV'
    MARCO = 'MAR'
    ABRIL = 'ABR'
    MAIO = 'MAI'
    JUNHO = 'JUN'
    JULHO = 'JUL'
    AGOSTO = 'AGO'
    SETEMBRO = 'SET'
    OUTUBRO = 'OUT'
    NOVEMBRO = 'NOV'
    DEZEMBRO = 'DEZ'
    MESES = (
        (JANEIRO, 'Janeiro'),
        (FEVEREIRO, 'Fevereiro'),
        (MARCO, 'Marco'),
        (ABRIL, 'Abril'),
        (MAIO, 'Maio'),
        (JUNHO, 'Junho'), 
        (JULHO, 'Julho'),
        (AGOSTO, 'Agosto'),
        (SETEMBRO, 'Setembro'),
        (OUTUBRO, 'Outubro'),
        (NOVEMBRO, '11'),
        (DEZEMBRO, '12'),
    )
    barco = models.ForeignKey(Controle_Embarcacao)
    meses = models.CharField(max_length=10, null=True, blank=True, choices=MESES)
    mes=models.CharField(max_length=10, null=True, blank=True)
    #mes = models.DateField(null=True, blank=True)
    receita_total = models.FloatField(null=True, blank=True)
    despesa_total = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.meses.__str__()


class Manutencao(models.Model):
    barco = models.ForeignKey(Controle_Embarcacao, null=True, blank=True)
    tipo = models.CharField(max_length=25)
    descricao = models.CharField(max_length=25)
    valor = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    
    
class Tripulacao(models.Model):
    barco = models.ForeignKey(Controle_Embarcacao, null=True, blank=True)
    nome = models.CharField(max_length=25, null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=15, null=True, blank=True)
    salario = models.FloatField(null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
  

            
class Controle_ArrecadacaoForm(ModelForm):
    class Meta: 
        model = Controle_Arrecadacao
        exclude = ()
        
class Controle_DespesasForm(ModelForm):
    class Meta:
        model = Controle_Despesas
        exclude = ()

class ManutencaoForm(ModelForm):
    class Meta: 
        model = Manutencao
        exclude = ()
        widgets = {
            'descricao': Textarea(attrs={'cols': 20, 'rows': 10}),
            }

class TripulacaoForm(ModelForm):
    class Meta:
        model = Tripulacao
        exclude = ()