'''
Created on 25 de nov de 2017

@author: rondy
'''
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from administrador.models import Controle_Despesas

User =  get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        
        if not user:
            raise forms.ValidationError("Usuario nao existe")
        if not user.check_password(password):
            raise forms.ValidationError("Senha incorreta")
        if not user.is_active:
            raise forms.ValidationError("Usuario nao ativo")
        return super(UserLoginForm, self).clean()

class DespesaForm(forms.Form):
    preco_combustivel = forms.FloatField()
        
    def clean(self):
        #barco = self.cleaned_data.get('barco')
        #data_viagem = self.cleaned_data.get('data_viagem')
        #qnt_combustivel = self.cleaned_data.get('qnt_combustivel')
        preco_combustivel = self.cleaned_data.get('preco_combustivel')
        # total_combustivel = self.cleaned_data.get('total_combustivel')
        
        return super(DespesaForm, self).clean()

class ControleForm(forms.Form):
    passageiros = forms.CharField()
    def clean(self): 
        passageiros = self.cleanead_data.get("passageiros-total")
        
        if not passageiros:
            raise forms.ValidationError("passageiro incorreto")
        
        return passageiros