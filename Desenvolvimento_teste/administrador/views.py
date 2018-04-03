from django.shortcuts import render, redirect, get_object_or_404
from .models import Controle_Arrecadacao, Controle_Despesas, Controle_Embarcacao, Controle_Usuario, Controle_Anual, Manutencao, Tripulacao
import datetime 

from django.forms import modelformset_factory
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.utils.formats import localize
import locale
from administrador.models import ManutencaoForm, Controle_ArrecadacaoForm, Controle_DespesasForm, TripulacaoForm
from django.utils.timezone import now
from _datetime import date
from ctypes.wintypes import PINT
# Create your views here.


@login_required(login_url='/login/')
def index(request):
    total = []
    qnt_passageiros = []
    total_despesas = []
    total_manutencao = []
    inicio = datetime.date(2018, 3, 1)
    fim = datetime.date(2018, 3, 31)
    Meses=('janeiro','fevereiro','Marco','abril','maio','junho',
          'julho','agosto','setembro','outubro','novembro','dezembro')
    
    agora = now()
    mes = (agora.month)
    mes_corrente = Meses[mes-1] 
    
    
    controle_usuario = Controle_Usuario.objects.select_related('user').filter(user=request.user)
    for c in controle_usuario:
        pass
    
    controle_arrecadacao = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes)
    for ca in controle_arrecadacao:
        total.append(ca.total)
        qnt_passageiros.append(ca.qnt_passagem)
    
    controle_despesas = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes)
    for cd in controle_despesas:
        total_despesas.append(cd.total)
    
    manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes)  
    for m in manutencao:
        total_manutencao.append(m.valor)
    
    locale.setlocale(locale.LC_ALL, '')
    
    #calculo da receita
    total_receita = sum(total)
    total_receita = locale.format('%.2f', total_receita, True)
    
    #calculo da despesa
    total_despesas = sum(total_despesas) 
    total_despesas = locale.format('%.2f', total_despesas, True) 
    
    #calculo da manutencao
    total_manutencao = sum(total_manutencao)
    total_manutencao = locale.format('%.2f', total_manutencao, True) 
    
    return render(request, 'administrador/index.html', {'total_mes':total_receita,
                                                        'qnt_passageiros':sum(qnt_passageiros),
                                                        'total_despesas':total_despesas,
                                                        'mes_corrente':mes_corrente,
                                                        'total_manutencao':total_manutencao}
                                                        )
    

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
    return render(request, "administrador/prototipo-login.html", {"form":form, "title":title})

def logout_view(request):
    logout(request)
    return redirect('index')
    
def controle_step(request):
    return render(request, "administrador/form-controle-step.html")

def manutencao(request):
    
    if request.method=='POST':
        manutencao = ManutencaoForm(request.POST)
        print(manutencao)
        if manutencao.is_valid():
            new_manutencao = manutencao.save(commit=False)
            new_manutencao.save()
            print(new_manutencao.pk) 
            return redirect('mt', pk=new_manutencao.pk)
    
    return render(request, "administrador/manutencao.html")

def confirmacao_manutencao(request, pk):
    print('confirmacao-detaill')
    manutencao = get_object_or_404(Manutencao, pk=pk)
    barco = Controle_Embarcacao.objects.get(user=request.user)
    
    return render(request, 'administrador/manutencao_v2.html', {'manutencao':manutencao,
                                                                'barco':barco})
def manutencao_edit(request, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    form = ManutencaoForm(request.POST or None, instance=manutencao)
    print("manutencao_edit")

    if request.method=='POST':
        new_form = form.save(commit=False)
        new_form.save()    
        return redirect('mt', manutencao.pk)
    
    return render(request, 'administrador/manutencao-edit.html', {'manutencao':manutencao,
                                                                  'form':form})


def tripulacao(request):
    if request.method=='POST':
        tripulacao = TripulacaoForm(request.POST)
        if tripulacao.is_valid():
            new_tripulacao = tripulacao.save(commit=False)
            new_tripulacao.save()
            
            return redirect('tripulacao-detail', pk=new_tripulacao.pk)
    
    return render(request, 'administrador/form-tripulacao.html')

def confirmacao_tripulacao(request, pk):
    print('confirmacao_tripulacao')
    tripulacao = get_object_or_404(Tripulacao, pk=pk)
    barco = Controle_Embarcacao.objects.get(user=request.user)
    print(tripulacao.nascimento)
    return render(request, 'administrador/tripulacao-detail.html', {'tripulacao':tripulacao,
                                                                    'barco':barco})
    
def tripulacao_edit(request, pk):
    tripulacao = get_object_or_404(Tripulacao, pk=pk)
    form = TripulacaoForm(request.POST or None, instance=tripulacao)

    if request.method=='POST':
        new_form = form.save(commit=False)
        new_form.save()    
        return redirect('tripulacao-detail', tripulacao.pk)
    
    return render(request, 'administrador/tripulacao-edit.html', {'tripulacao':tripulacao,
                                                                  'form':form})

@login_required(login_url='/login/')
def controle(request):

    if request.method=='POST':
        #barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
        barco = Controle_Embarcacao.objects.get(user=request.user)        
        receita = Controle_ArrecadacaoForm(request.POST)
        print(receita)
        if receita.is_valid():
            print("is_valid")
            new_receita = receita.save(commit=False)
            new_receita.barco = barco
            new_receita.save()
            return redirect('receita-detail', pk=new_receita.pk)
    
    return render(request, 'administrador/form-controle.html')
#===============================================================================
# def controle(request):
#     data_viagem = request.POST.get('data_viagem')
#     passageiros_total = request.POST.get('passageiros-total')
#     passageiros_inteira = request.POST.get('passageiros-inteira')
#     passageiros_meia = request.POST.get('passageiros-meia')
#     receita_alimentacao = request.POST.get('receita-alimentacao')
#     encomendas = request.POST.get('encomendas')
#     cargas = request.POST.get('cargas')
#     outras_receitas = request.POST.get('outras-receitas')
#     barco = Controle_Usuario.objects.select_related('barco').filter(user=request.user)
#     
#     p = ControleForm()
#     if request.method=='POST':
#         p = p.clean()
#         print(p)
#         total_receita = int(passageiros_inteira) + int(passageiros_meia)
#         
#         for b in barco:
#             pass
#             
#         controle_arrecadacao = Controle_Arrecadacao(barco=b.barco, 
#                                                     data_viagem=data_viagem,
#                                                     qnt_passagem=passageiros_total,
#                                                     qnt_adulto=passageiros_inteira,
#                                                     qnt_crianca=passageiros_meia,
#                                                     alimentacao=receita_alimentacao,
#                                                     encomendas=encomendas,
#                                                     outros=outras_receitas,
#                                                     total=total_receita)
# 
#         controle_arrecadacao.save()
#         controle_receita = Controle_Arrecadacao.objects.select_related('barco').filter(barco=b.barco)
#         for c in controle_receita:
#             pass
#         
#         Controle_Anual.objects.filter(mes=c.data_viagem.month).update(mes=c.data_viagem.month,
#                                                                       receita_total=c.total)
#             
#         
#         return redirect('receita-detail', pk=controle_arrecadacao.pk)
#     
#     else:
#         print("controle/else")       
#         return render(request, 'administrador/form-controle.html')
#===============================================================================


@login_required(login_url='/login/')
def receita_detail(request, pk):
    receita = get_object_or_404(Controle_Arrecadacao, pk=pk)
    print("receita_detail")
    if request.method=='POST':
        print("receita_detail/POST")
        data_viagem = request.POST.get('data_viagem')
        passageiros_total = request.POST.get('passageiros-total')
        passageiros_inteira = request.POST.get('passageiros-inteira')
        passageiros_meia = request.POST.get('passageiros-meia')
        receita_alimentacao = request.POST.get('receita-alimentacao')
        encomendas = request.POST.get('encomendas')
        cargas = request.POST.get('cargas')
        outras_receitas = request.POST.get('outros')
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
    form = Controle_ArrecadacaoForm(request.POST or None, instance=receita)
    print("receita_edit")
    print(receita.barco)
    print(form)
    if request.method=='POST':
        print("receita_edit/POST")
        new_form = form.save(commit=False)
        new_form.barco = Controle_Embarcacao.objects.get(user=request.user)
        new_form.save()
        
        return redirect('receita-detail', receita.pk)
    
    return render(request, 'administrador/receita-edit.html', {'receita':receita,
                                                               'form':form}) 

@login_required(login_url='/login/')
def controle_despesas(request):
    if request.method=='POST':
        barco = Controle_Embarcacao.objects.get(user=request.user)
        despesas = Controle_DespesasForm(request.POST)
        print(despesas)
        if despesas.is_valid():
            new_despesas = despesas.save(commit=False)
            new_despesas.barco = barco
            new_despesas.save()
            
            return redirect('despesa-detail', pk=new_despesas.pk)
    
    return render(request, 'administrador/form-despesas.html')


@login_required(login_url='/login/')                         
def despesa_detail(request, pk):
    despesa = get_object_or_404(Controle_Despesas, pk=pk)
    print("combustive:",despesa.qnt_combustivel)
    if request.method=="POST":
        data_viagem = request.POST.get('data_viagem')
        despesas_qnt_combustivel = request.POST.get('qnt_combustivel')
        despesas_preco_combustivel = request.POST.get('preco_combustivel')
        despesas_total_combustivel = request.POST.get('total_combustivel')
        despesas_tripulacao = request.POST.get('tripulacao')
        despesas_alimentacao = request.POST.get('alimentacao')
        outras_despesas = request.POST.get('outros')
        
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
        
        print("despesa_detail/else")
        return render(request, 'administrador/despesa-detail.html', {'despesa':despesa})
    
    print("despesa_detail/return")
    return render(request, 'administrador/form-despesas.html')

def despesa_edit(request, pk): 
    despesa = get_object_or_404(Controle_Despesas, pk=pk) 
    form = Controle_DespesasForm(request.POST or None, instance=despesa)
    print("despesa_edit/despesa:")
    if request.method=='POST':  
        print('despesa_edit/POST')
        form.save()
        return redirect('despesa-detail', despesa.pk)
    return render(request, 'administrador/despesa-edit.html', {'despesa':despesa,
                                                               'form':form})    
    

def confirmacao_controle(request, pk_receita, pk_despesa):
    
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

def detalhar_receita_admin(request):
    print('detalhar_receita_admin')
    total_manutencao = []
    total_receita = []
    total_despesa = []
    total_passageiros = []
    Meses=('janeiro','fevereiro','Marco','abril','maio','junho',
          'julho','agosto','setembro','outubro','novembro','dezembro')
    agora = now()
    mes_hj = (agora.month) 
    mes_corrente = Meses[mes_hj-1]
    manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes_hj)
    receitas = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    despesas = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    
    for r in receitas:
        total_receita.append(r.total)
        total_passageiros.append(r.qnt_passagem)
    total_receita = sum(total_receita)
    total_passageiros = sum(total_passageiros)
    
    for d in despesas:
        total_despesa.append(d)
    total_despesa = sum(total_despesa)
       
    for m in manutencao:
        total_manutencao.append(m.valor)
    total_manutencao = sum(total_manutencao)
    
    return render(request, 'administrador/admin-receita-detail.html', {   'receita':receitas,
                                                                          'mes_corrente':mes_corrente,
                                                                          'total_manutencao':total_manutencao,
                                                                          'total_receita':total_receita,
                                                                          'total_despesa':total_despesa,
                                                                          'total_passageiros':total_passageiros})

def detalhar_passagem_admin(request):
    print('detalhar_passageiro_admin')
    total_manutencao = []
    total_receita = []
    total_despesa = []
    total_passageiros = []
    Meses=('janeiro','fevereiro','Marco','abril','maio','junho',
          'julho','agosto','setembro','outubro','novembro','dezembro')
    agora = now()
    mes_hj = (agora.month) 
    mes_corrente = Meses[mes_hj-1]
    manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes_hj)
    receitas = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    despesas = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    
    for r in receitas:
        total_receita.append(r.total)
        total_passageiros.append(r.qnt_passagem)
    total_receita = sum(total_receita)
    total_passageiros = sum(total_passageiros)
    
    for d in despesas:
        total_despesa.append(d)
    total_despesa = sum(total_despesa)
       
    for m in manutencao:
        total_manutencao.append(m.valor)
    total_manutencao = sum(total_manutencao)
    
    return render(request, 'administrador/admin-passagem-detail.html', {  'passagens':receitas,
                                                                          'mes_corrente':mes_corrente,
                                                                          'total_manutencao':total_manutencao,
                                                                          'total_receita':total_receita,
                                                                          'total_despesa':total_despesa,
                                                                          'total_passageiros':total_passageiros})

def detalhar_despesas_admin(request):
    print('detalhar_despesas_admin')
    total_manutencao = []
    total_receita = []
    total_despesa = []
    total_passageiros = []
    Meses=('janeiro','fevereiro','Marco','abril','maio','junho',
          'julho','agosto','setembro','outubro','novembro','dezembro')
    agora = now()
    mes_hj = (agora.month) 
    mes_corrente = Meses[mes_hj-1]
    manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes_hj)
    receitas = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    despesas = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    
    for r in receitas:
        total_receita.append(r.total)
        total_passageiros.append(r.qnt_passagem)
    total_receita = sum(total_receita)
    total_passageiros = sum(total_passageiros)
    
    for d in despesas:
        total_despesa.append(d)
    total_despesa = sum(total_despesa)
       
    for m in manutencao:
        total_manutencao.append(m.valor)
    total_manutencao = sum(total_manutencao)
    
    return render(request, 'administrador/admin-despesa-detail.html', {   'despesas':despesas,
                                                                          'mes_corrente':mes_corrente,
                                                                          'total_manutencao':total_manutencao,
                                                                          'total_receita':total_receita,
                                                                          'total_despesa':total_despesa,
                                                                          'total_passageiros':total_passageiros})


def detalhar_manutencoes_admin(request):
    print('detalhar_manutencoes_admin')
    total_manutencao = []
    total_receita = []
    total_despesa = []
    total_passageiros = []
    Meses=('janeiro','fevereiro','Marco','abril','maio','junho',
          'julho','agosto','setembro','outubro','novembro','dezembro')
    agora = now()
    mes_hj = (agora.month) 
    mes_corrente = Meses[mes_hj-1]
    manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes_hj)
    receitas = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    despesas = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes_hj)
    
    for r in receitas:
        total_receita.append(r.total)
        total_passageiros.append(r.qnt_passagem)
    total_receita = sum(total_receita)
    total_passageiros = sum(total_passageiros)
    
    for d in despesas:
        total_despesa.append(d)
    total_despesa = sum(total_despesa)
       
    for m in manutencao:
        total_manutencao.append(m.valor)
    total_manutencao = sum(total_manutencao)
    
    return render(request, 'administrador/admin-manutencao-detail.html', {'manutencao':manutencao, 
                                                                          'mes_agora':mes_corrente,
                                                                          'total_manutencao':total_manutencao,
                                                                          'total_receita':total_receita,
                                                                          'total_despesa':total_despesa,
                                                                          'total_passageiros':total_passageiros})

def tables_tripulation(request):
    print('admin_tripulacao')
    tripulation = Tripulacao.objects.select_related('barco')
    print(tripulation)
    #barco = Controle_Embarcacao.objects.get(user=request.user)
    
    return render(request, 'administrador/tables_tripulation.html', {'tripulation':tripulation})


def form_google(request):
    return render(request, 'administrador/form-google.html')
    
      
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
        data_viagem = []
        receita_total = []
        despesa_total = []
        receita_mes = []
        passagens_total = []
        passagens_inteira = []
        passagens_meia = []
        list_mes = []
        dic = {}
        mes = []
        valor = []
        c = {}
        tipo_total = {}
        
        agora = now()
        mes_hj = (agora.month)
        
        ca = Controle_Arrecadacao.objects.select_related('barco').filter(data_viagem__month=mes_hj)
        despesas_total = Controle_Despesas.objects.select_related('barco').filter(data_viagem__month=mes_hj)
        manutencao = Manutencao.objects.select_related('barco').filter(data__month=mes_hj)
      
        #manutençao
        for m in manutencao:
            if m.tipo not in tipo_total:
                tipo_total[m.tipo] = m.valor
            else:
                tipo_total[m.tipo] = tipo_total[m.tipo] + m.valor
            
        manutencao_total =  sum(tipo_total.values())
        
        #Despesas
        for des in despesas_total:
            despesa_total.append(des.total)
        
        despesas = sum(despesa_total)
        
        #Controle_arrecadacao
        for d in ca:
            c[d.data_viagem]=d.total
            passagens_total.append(d.qnt_passagem)
            passagens_inteira.append(d.qnt_adulto)
            passagens_meia.append(d.qnt_crianca)
        print("inteira",passagens_inteira)  
        print("meia",passagens_meia) 
        for s in sorted(c.items()):
            data_viagem.append(s[0])
            receita_total.append(s[1])
        
        receita = sum(receita_total)
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
            "tipo":tipo_total.keys(),
            "valores_manutencao":tipo_total.values(),
            "manutencao":manutencao_total,
            "despesa":despesas,
            "receita":receita,
            "pass_total":passagens_total,
            "pass_inteira":passagens_inteira,
            "pass_meia":passagens_meia
                    
        }
        return Response(data)
