from django.shortcuts import render, redirect, get_object_or_404
from .models import Controle_Arrecadacao, Controle_Despesas, Controle_Embarcacao, Controle_Usuario, Controle_Anual, Manutencao
from django.http.response import JsonResponse
import datetime 
import collections

from django.forms import modelformset_factory
from .forms import UserLoginForm, DespesaForm, ControleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User, Group
from django.db.models import Sum
from datetime import date
from django.utils.formats import localize
import locale
from administrador.models import ManutencaoForm
# Create your views here.


@login_required(login_url='/login/')
def index(request):
    total = []
    qnt_passageiros = []
    
    controle_usuario = Controle_Usuario.objects.select_related('user').filter(user=request.user)

    for c in controle_usuario:
        pass
    
    controle_arrecadacao = Controle_Arrecadacao.objects.select_related('barco').filter(barco=c.barco)
    for ca in controle_arrecadacao:
        total.append(ca.total)
        qnt_passageiros.append(ca.qnt_passagem)
    
    valor = sum(total)
    locale.setlocale(locale.LC_ALL, '')
    valor = locale.format('%.2f', valor, True) 
    print (valor)
    return render(request, 'administrador/index.html', {'total_mes':valor,
                                                        'qnt_passageiros':sum(qnt_passageiros)}
                                                        )

@login_required(login_url='/login/')
def charts(request):
    total = []
    total2 = [1000, 2000, 3000]
    arrecadacao = Controle_Arrecadacao.objects.all()
    for a in arrecadacao:
        total.append(a.total)
        
    return render(request, 'administrador/charts.html', {'total':total,
                                                         'total2':total2})
def get_data(request):
    data={
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)
    
def tables(request):
    return render(request, 'administrador/tables.html')

def login_view(request):
    title = "login"
    #next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        #if next:
        #    return redirect(next)
        #print(user.get_group_permissions())
        if user.has_perm("auth.change_permission"):
            return redirect("/administrador/index")
        else:
            return redirect("/administrador/formulario-controle")
    return render(request, "administrador/login.html", {"form":form, "title":title})

def logout_view(request):
    logout(request)
    return redirect('index')
    
def controle_step(request):
    return render(request, "administrador/form-controle-step.html")

def prototipo_manutencao(request):
    descricao = ManutencaoForm(request.POST)
    ManutencaoFormSet = modelformset_factory(Manutencao, exclude=())
    if request.method=='POST':
        print("post")
        print(descricao)
        if descricao.is_valid():
            print("is_valid")
            descricao.save()
            r = Manutencao.objects.all()
            formset = ManutencaoFormSet()

            return render(request, "administrador/manutencao.html", {"descricao":descricao,
                                                                               "r":r,
                                                                               "formset":formset})
    
    return render(request, "administrador/manutencao.html")

@login_required(login_url='/login/')
def controle(request):
    data_viagem = request.POST.get('data_viagem')
    passageiros_total = request.POST.get('passageiros-total')
    passageiros_inteira = request.POST.get('passageiros-inteira')
    passageiros_meia = request.POST.get('passageiros-meia')
    receita_alimentacao = request.POST.get('receita-alimentacao')
    encomendas = request.POST.get('encomendas')
    cargas = request.POST.get('cargas')
    outras_receitas = request.POST.get('outras-receitas')
    barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
    
    p = ControleForm()
    if request.method=='POST':
        p = p.clean()
        print(p)
        total_receita = int(passageiros_inteira) + int(passageiros_meia)
        
        for b in barco:
            pass
            
        controle_arrecadacao = Controle_Arrecadacao(barco=b.barco, 
                                                    data_viagem=data_viagem,
                                                    qnt_passagem=passageiros_total,
                                                    qnt_adulto=passageiros_inteira,
                                                    qnt_crianca=passageiros_meia,
                                                    alimentacao=receita_alimentacao,
                                                    encomendas=encomendas,
                                                    outros=outras_receitas,
                                                    total=total_receita)

        controle_arrecadacao.save()
        controle_receita = Controle_Arrecadacao.objects.select_related('barco').filter(barco=b.barco)
        for c in controle_receita:
            pass
        
        Controle_Anual.objects.filter(mes=c.data_viagem.month).update(mes=c.data_viagem.month,
                                                                      receita_total=c.total)
            
        
        return redirect('receita-detail', pk=controle_arrecadacao.pk)
    
    else:
        print("controle/else")       
        return render(request, 'administrador/form-controle.html')


@login_required(login_url='/login/')
def receita_detail(request, pk):
    receita = get_object_or_404(Controle_Arrecadacao, pk=pk)
    
    print("receita_detail")
    
    if request.method=='POST':
        data_viagem = request.POST.get('data_viagem')
        passageiros_total = request.POST.get('passageiros-total')
        passageiros_inteira = request.POST.get('passageiros-inteira')
        passageiros_meia = request.POST.get('passageiros-meia')
        receita_alimentacao = request.POST.get('receita-alimentacao')
        encomendas = request.POST.get('encomendas')
        cargas = request.POST.get('cargas')
        outras_receitas = request.POST.get('outras-receitas')
        total_receita = int(passageiros_inteira) + int(passageiros_meia)
            
        controle_arrecadacao = Controle_Arrecadacao(barco=receita.barco, 
                                                    data_viagem=data_viagem,
                                                    qnt_passagem=passageiros_total,
                                                    qnt_adulto=passageiros_inteira,
                                                    qnt_crianca=passageiros_meia,
                                                    alimentacao=receita_alimentacao,
                                                    encomendas=encomendas,
                                                    outros=outras_receitas,
                                                    total=total_receita)

        controle_arrecadacao.save()
        print("controle/redirect")
        return redirect('receita-detail', pk=controle_arrecadacao.pk)
             
    else:
        
        print("receita_detail/else")
        return render(request, 'administrador/receita-detail.html', {'receita':receita})
    
    print("receita_detail/return")
    return render(request, 'administrador/form-controle.html')
    
def receita_edit(request, pk):
    receita = get_object_or_404(Controle_Arrecadacao, pk=pk)
    #print(receita.alimentacao)
    if request.method=='POST':
        data_viagem = request.POST.get('data_viagem')
        passageiros_total = request.POST.get('passageiros-total')
        passageiros_inteira = request.POST.get('passageiros-inteira')
        passageiros_meia = request.POST.get('passageiros-meia')
        receita_alimentacao = float(request.POST.get('receita-alimentacao'))
        encomendas = float(request.POST.get('encomendas'))
        cargas = float(request.POST.get('cargas'))
        outras_receitas = float(request.POST.get('outras-receitas'))
        total_receita = int(passageiros_inteira) + int(passageiros_meia)
        
        controle_receita = Controle_Arrecadacao.objects.filter(pk=receita.pk).update(data_viagem=data_viagem,
                                                    qnt_passagem=passageiros_total,
                                                    qnt_adulto=passageiros_inteira,
                                                    qnt_crianca=passageiros_meia,
                                                    alimentacao=receita_alimentacao,
                                                    encomendas=encomendas,
                                                    outros=outras_receitas,
                                                    total=total_receita)
        
        return redirect('receita-detail', receita.pk)
    
    return render(request, 'administrador/receita-edit.html', {'receita':receita}) 

@login_required(login_url='/login/')
def controle_despesas(request):
    data_viagem = request.POST.get('data_viagem')
    despesas_qnt_combustivel = request.POST.get('qnt-combustivel')
    despesas_preco_combustivel = request.POST.get('preco-combustivel')
    despesas_total_combustivel = request.POST.get('total-combustivel')
    despesas_tripulacao = request.POST.get('despesas-tripulacao')
    despesas_alimentacao = request.POST.get('despesas-alimentacao')
    outras_despesas = request.POST.get('outras-despesas')
    barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
    
    if request.method=='POST':
        total_despesas = int(despesas_total_combustivel) + int(despesas_alimentacao)
        for b in barco:
            pass
        controle_despesas = Controle_Despesas(barco=b.barco,
                                                  data_viagem=data_viagem,
                                                  qnt_combustivel=despesas_qnt_combustivel,
                                                  preco_combustivel=despesas_preco_combustivel,
                                                  total_combustivel=despesas_total_combustivel,
                                                  tripulacao=despesas_tripulacao,
                                                  alimentacao=despesas_alimentacao,
                                                  outros=outras_despesas,
                                                  total=total_despesas)
        controle_despesas.save()      
        return redirect('despesa-detail', pk=controle_despesas.pk)
    else:
        return render(request, 'administrador/form-despesas.html')

@login_required(login_url='/login/')                         
def despesa_detail(request, pk):
    despesa = get_object_or_404(Controle_Despesas, pk=pk)
    
    if request.method=="POST":
        data_viagem = request.POST.get('data_viagem')
        despesas_qnt_combustivel = request.POST.get('qnt-combustivel')
        despesas_preco_combustivel = float(request.POST.get('preco-combustivel'))
        despesas_total_combustivel = float(request.POST.get('total-combustivel'))
        despesas_tripulacao = float(request.POST.get('despesas-tripulacao'))
        despesas_alimentacao = float(request.POST.get('despesas-alimentacao'))
        outras_despesas = float(request.POST.get('outras-despesas'))
        
        barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
        
        total_despesas = int(despesas_total_combustivel) + int(despesas_alimentacao)
        
        controle_despesas = Controle_Despesas(barco=despesa.barco,
                                                  data_viagem=data_viagem,
                                                  qnt_combustivel=despesas_qnt_combustivel,
                                                  preco_combustivel=despesas_preco_combustivel,
                                                  total_combustivel=despesas_total_combustivel,
                                                  tripulacao=despesas_tripulacao,
                                                  alimentacao=despesas_alimentacao,
                                                  outros=outras_despesas,
                                                  total=total_despesas)
        controle_despesas.save()      
        return redirect('despesa-detail', pk=controle_despesas.pk)
             
    else:
        
        print("receita_detail/else")
        return render(request, 'administrador/despesa-detail.html', {'despesa':despesa})
    
    print("despesa_detail/return")
    return render(request, 'administrador/form-despesas.html')

def despesa_edit(request, pk): 
    despesa = get_object_or_404(Controle_Despesas, pk=pk) 
    
    if request.method=="POST":
        data_viagem = request.POST.get('data_viagem')
        despesas_qnt_combustivel = request.POST.get('qnt-combustivel')
        despesas_preco_combustivel = request.POST.get('preco-combustivel')
        despesas_total_combustivel = request.POST.get('total-combustivel')
        despesas_tripulacao = request.POST.get('despesas-tripulacao')
        despesas_alimentacao = request.POST.get('despesas-alimentacao')
        outras_despesas = request.POST.get('outras-despesas')
        barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
        
        total_despesas = int(despesas_total_combustivel) + int(despesas_alimentacao)
        
        controle_despesa = Controle_Despesas.objects.filter(pk=despesa.pk).update(barco=despesa.barco,
                                                                                  data_viagem=data_viagem,
                                                                                  qnt_combustivel=despesas_qnt_combustivel,
                                                                                  preco_combustivel=despesas_preco_combustivel,
                                                                                  total_combustivel=despesas_total_combustivel,
                                                                                  tripulacao=despesas_tripulacao,
                                                                                  alimentacao=despesas_alimentacao,
                                                                                  outros=outras_despesas,
                                                                                  total=total_despesas
                                                                                 )
    
        return redirect('despesa-detail', despesa.pk)
    return render(request, 'administrador/despesa-edit.html', {'despesa':despesa}) 

def confirmacao_controle(request, pk_receita, pk_despesa):
    #controle_arrecadacao = Controle_Arrecadacao.objects.get(pk=pk_receita)
    #controle_despesas = Controle_Despesas.objects.get(pk=pk_despesa)
    receita = get_object_or_404(Controle_Arrecadacao, pk=pk_receita)
    despesa = get_object_or_404(Controle_Despesas, pk=pk_despesa)
    
    if request.method=="POST":
        form_receita = Controle_Arrecadacao(request.POST, instance=receita)
        form_despesa = Controle_Despesas(request.POST, instance=despesa)
        if form_receita.is_valid() and form_despesa.is_valid():
            form_receita.save()
            form_despesa.save()
            return render(request, "administrador/manutencao-registrar.html", {'receita':receita,
                                                                               'despesas':despesa}) 
    else:
        form_receita = Controle_Arrecadacao(instance=receita)
        form_despesa = Controle_Despesas(instance=despesa)
    
    return render(request, 'administrador/controle-edit.html',)

def form_google(request):
    return render(request, 'administrador/form-google.html')


def manutencao_registrar(request):
    return render(request, 'administrador/manutencao-registrar.html')

def tripulacao_registrar(request):
    return render(request, 'administrador/tripulacao-registrar.html')

      
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Orange" ]
        default_itens = [qs_count, 10, 12, 14, 16]
        data = {
            
            "labels": labels,
            "default_itens":default_itens,
            "customers": qs_count,
            
        }
        return Response(data)

class ChartLineData(APIView):
    
    def get(self, request, format=None):
        inicio = datetime.date(2017, 12, 1)
        fim = datetime.date(2017, 12, 31)
        data_viagem = []
        receita_total = []
        meses = []
        receita_mes = []
        list_mes = []
        dic = {}
        mes = []
        valor = []
        c = {}
       
        ca = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__range=(inicio, fim))
        
        for d in ca:
            c[d.data_viagem]=d.total
        
        for s in sorted(c.items()):
           data_viagem.append(s[0])
           receita_total.append(s[1])
        
        
        mes_total =  Controle_Anual.objects.select_related('barco')
        for m in mes_total:
            dic[int(m.mes)] = m.receita_total
        
        for v in sorted(list(dic.items())):
            list_mes.append(v)
        
        for k, v in list_mes:
            mes.append(k)
            valor.append(v)
        
        data = {
            
            "viagem_data": data_viagem,
            "receita_total":receita_total,
            "receita_mes":receita_mes,
            "valor":valor,
            "meses":meses,
               
        }
        return Response(data)
