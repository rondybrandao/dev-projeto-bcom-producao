from django.shortcuts import render, redirect, get_object_or_404
from .models import Viagem, Compra, Carrinho, Passagem, Poltrona

from django.template.context_processors import request
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from xml.dom.minidom import parse

from django.views.decorators.http import require_http_methods
from django.db import transaction

import xml.etree.ElementTree as ET
import requests
import decimal
from imaplib import Response_code
from itertools import count

from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem
from pagseguro.signals import checkout_realizado
from pagseguro.signals import notificacao_recebida

from .exceptions import CheckoutException
from rest_framework.utils import json
from pagseguro.settings import PAYMENT_URL
from _ast import Num



# Create your views here.

def index(request):
    
    return render(request, 'dev_radioanori/index.html')


def index_old(request):
    origem_entrada = request.POST.get('sel1')
    qnt_inteira = request.POST.get('adulto')
    qnt_meia = request.POST.get('crianca')
    if request.method=='POST':
        viagem = Viagem.objects.filter(origem=origem_entrada)
        for v in viagem:
            #passagem = Compra(viagem = v, qnt_adulto=qnt_adulto, qnt_crianca=qnt_crianca, nome_passageiro="rondy")
            carrinho = Carrinho(viagem = v, qnt_inteira=qnt_inteira, qnt_meia=qnt_meia)
            carrinho.save()
            
            return redirect('carrinho', pk=carrinho.pk) 
        
    return render(request, 'dev_radioanori/index.html')

#===============================================================================
# def carrinho(request, pk):
#     passagem = get_object_or_404(Compra, pk=pk)
#     total = (int(passagem.qnt_adulto) * passagem.viagem.preco_adulto) + (int(passagem.qnt_crianca) * passagem.viagem.preco_crianca)
#     
#     if request.method=='POST':
#         carrinho = Carrinho(compra=passagem, total=total)
#         carrinho.save()
#         print(request)
#         return redirect('carrinho_detalhe', pk=carrinho.pk)
#         
#     else:
#         if request.method=='GET':
#             nova_origem = request.GET.get('sel1')
#             print(nova_origem)
#             try:
#                 viagem = Viagem.objects.filter(origem=nova_origem)
#                 for v in viagem:
#                     passagem = Compra.objects.filter(pk=pk).update(viagem=v.pk)
#                     passagem = get_object_or_404(Compra, pk=pk)
#                     passagem.save()
#                 return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
#                                                                 'total': total})
#             except Viagem.DoesNotExist:
#                 pass 
#                 
#     return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
#                                                                 'total': total})
#===============================================================================
#===============================================================================
# def carrinho(request, pk):
#     #compra = get_object_or_404(Compra, pk=pk)
#     carrinho = get_object_or_404(Carrinho, pk=pk)
#     print("carrinho", carrinho.pk)
#     print("carrinho inteira antes", carrinho.qnt_inteira)
#     print("carrinho antes total", carrinho.total)
#     
#     total = (int(carrinho.qnt_inteira) * carrinho.viagem.preco_adulto) + (int(carrinho.qnt_meia) * carrinho.viagem.preco_crianca)
#     #total = (int(compra.qnt_adulto) * compra.viagem.preco_adulto) + (int(compra.qnt_crianca) * compra.viagem.preco_crianca)
#     
#     if request.method=='POST':
#         #carrinho = Carrinho(compra=compra, total=total)
#         carrinho.save()
#         print("POST", request)
#         return redirect('escolher-poltrona', pk=carrinho.pk)
#         
#     
#     elif request.method=='GET':
#         nova_origem = request.GET.get('sel1')
#         nome = request.GET.get('nome')
#         inteira = request.GET.get('inteira')
#         print("GET")
#         print("inteira depois", inteira)
#         try:
#             viagem = Viagem.objects.filter(origem=nova_origem)
#             for v in viagem:
#                 passagem = Carrinho.objects.filter(pk=pk).update(viagem=v.pk)
#                 passagem = get_object_or_404(Carrinho, pk=pk)
#                 print(passagem)
#                 passagem.save()
#                 
#             if inteira != None:
#                 print("if not None") 
#                 Carrinho.objects.filter(pk=pk).update(qnt_inteira=inteira)
#                 new_carrinho = get_object_or_404(Carrinho, pk=pk)
#                 new_carrinho.save()
#                 print("new-carrinho", new_carrinho)
#                 
#                 print("carrinho.inteira", carrinho.qnt_inteira)
#                 print("carrinho.pk", carrinho.pk)
#                 print("carrinho.total", carrinho.total)
#                 return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':carrinho,'nome':nome, 'inteira':inteira,
#                                                                             'total': total})
#             else:
#                 print("if None") 
#                 Carrinho.objects.filter(pk=pk).update(qnt_inteira=carrinho.qnt_inteira)
#                 new_carrinho = get_object_or_404(Carrinho, pk=pk)
#                 new_carrinho.save()
#                 print("new-carrinho", new_carrinho)
#                 return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':carrinho,'nome':nome, 'inteira':inteira,
#                                                                             'total': total})
#                     
#             return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':carrinho,'nome':nome, 'inteira':inteira,
#                                                                             'total': total})
#         except Viagem.DoesNotExist:
#                 pass 
#                 
#     return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
#                                                                 'total': 'POST'})
#===============================================================================
#===============================================================================
# def carrinho(request, pk):
#     carrinho = get_object_or_404(Carrinho, pk=pk)
#     print("carrinho", carrinho.pk)
#     print("carrinho inteira antes", carrinho.qnt_inteira)
#     print("carrinho antes total", carrinho.total)
#      
#     total = (int(carrinho.qnt_inteira) * carrinho.viagem.preco_adulto) + (int(carrinho.qnt_meia) * carrinho.viagem.preco_crianca)
#     #total = (int(compra.qnt_adulto) * compra.viagem.preco_adulto) + (int(compra.qnt_crianca) * compra.viagem.preco_crianca)
#      
#     if request.method=='POST':
#         #carrinho = Carrinho(compra=compra, total=total)
#         carrinho.save()
#         print("POST", request)
#         return redirect('escolher-poltrona', pk=carrinho.pk)
#          
#      
#     else: 
#         nova_origem = request.GET.get('sel1')
#         nome = request.GET.get('nome')
#         inteira = request.GET.get('inteira')
#         print("GET")
#         print("inteira depois", inteira)
#         try:
#             viagem = Viagem.objects.filter(origem=nova_origem)
#             for v in viagem:
#                 passagem = Carrinho.objects.filter(pk=pk).update(viagem=v.pk)
#                 passagem = get_object_or_404(Carrinho, pk=pk)
#                 print(passagem)
#                 passagem.save()
#                  
#             if inteira != None:
#                 print("if not None") 
#                 Carrinho.objects.filter(pk=pk).update(qnt_inteira=inteira, total=total)
#                 new_carrinho = get_object_or_404(Carrinho, pk=pk)
#                 new_carrinho.save()
#                 print("new-carrinho", new_carrinho)
#                 print("new-carrinho.inteira", new_carrinho.qnt_inteira)
#                 print("new-carrinho.total", new_carrinho.total)
#                  
#                 print("carrinho.inteira", carrinho.qnt_inteira)
#                 print("carrinho.pk", carrinho.pk)
#                 print("carrinho.total", carrinho.total)
#                 return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':new_carrinho,'nome':nome, 'inteira':new_carrinho.qnt_inteira,
#                                                                             'total': new_carrinho.total})
#             else:
#                 print("if None") 
#                 Carrinho.objects.filter(pk=pk).update(qnt_inteira=carrinho.qnt_inteira, total=total)
#                 new_carrinho = get_object_or_404(Carrinho, pk=pk)
#                 new_carrinho.save()
#                 print("new-carrinho", new_carrinho)
#                 print("new-carrinho.total", new_carrinho.total)
#                 return redirect( 'carrinho', {'passagem':new_carrinho,'nome':nome, 'inteira':inteira,
#                                                                             'total': total})
#                      
#             return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':carrinho,'nome':nome, 'inteira':inteira,
#                                                                             'total': total})
#         except Viagem.DoesNotExist:
#                 pass 
#                  
#     return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
#                                                                 'total': 'POST'})
#===============================================================================

#===============================================================================
# def pesquisar_viagens(request):
#     print("pesquisar viagem")
#     origem = request.POST.get('origem')
#     destino = request.POST.get('destino')
#     data_da_viagem = request.POST.get('data_viagem')
#     qnt_inteira = request.POST.get('inteira') 
#     qnt_meia = request.POST.get('meia')
#     viagem_dic = {}
#     
#     if request.method=='POST':
#         print("pesquisar/POST")
#         viagem = Viagem.objects.filter(origem=origem)
#             
#         for v in viagem:
#             total=(v.preco_adulto * float(qnt_inteira) + v.preco_crianca * float(qnt_meia))
#             viagem_dic[v]=total
#             qnt_passagens = int(qnt_inteira) + int(qnt_meia)
#             
#             #===================================================================
#             # print("inteira",qnt_inteira)
#             # print("meia",qnt_meia)
#             # print(qnt_passagens)
#             #===================================================================
#             
#         return render(request, 'dev_radioanori/lista_viagem.html',{'viagem':viagem_dic, 'total':viagem_dic.values(), 'origem':origem, 
#                                                                     'destino':destino, 'inteira':qnt_inteira, 'meia':qnt_meia, 'passagens':qnt_passagens})
#===============================================================================

def pesquisar_viagens(request):
    origem = request.POST.get('origem')  
    qnt_inteira = request.POST.get('inteira') 
    qnt_meia = request.POST.get('meia')
    viagem_dic = {}
    carrinho_dic = {}
    code_dic = {}
    qnt_passagens = []
    if request.method=='POST':
        print("POST")
        viagem = Viagem.objects.filter(origem=origem)
         
        for v in viagem:
            total=(v.preco_adulto * int(qnt_inteira) + v.preco_crianca * int(qnt_meia))
            carrinho = Carrinho.objects.create(viagem=v, qnt_inteira=qnt_inteira, qnt_meia=qnt_meia, total=total)
            carrinhoId = carrinho.pk
            viagem_dic[v]=total
            qnt_passagens=(int(qnt_inteira) + int(qnt_meia))
            carrinhoDescricao = v.origem + '-' + v.destino
            carrinhoAmount1 = v.preco_adulto
            preco_pago = total
            preco_original = v.preco_adulto * qnt_passagens
            r = (preco_pago/preco_original) * 100
            des = 100 - r
            numero_decimal = '{:.2f}'.format(des)
             
            #DISCOUNT_PERCENT=numero_decimal
             
            print(carrinhoId, total, carrinhoDescricao)
            sessions = {
                'email':'rondynely@hotmail.com',
                'token':'9F7A75D37B074BF4812D45CA5091ABEC',
                }
             
            response = requests.post('https://ws.pagseguro.uol.com.br/v2/sessions',data=sessions)           
            root = ET.fromstring(response.text)
            code=root[0].text
            carrinho_dic[carrinho]=code
           
         
        context= {'carrinho':carrinho_dic,
                  'code':code_dic,
                  'viagem':viagem_dic,
                  'qnt_passagens':qnt_passagens}
         
        return render(request, 'dev_radioanori/lista-viagem-prototipo2.html', context)

#===============================================================================
# def pesquisar_viagens(request):
#     origem = request.POST.get('origem')  
#     qnt_inteira = request.POST.get('inteira') 
#     qnt_meia = request.POST.get('meia')
#     viagem_dic = {}
#     carrinho_dic = {}
#     code_dic = {}
#     qnt_passagens = []
#     if request.method=='POST':
#         print("POST")
#         viagem = Viagem.objects.filter(origem=origem)
#         
#         for v in viagem:
#             total=(v.preco_adulto * int(qnt_inteira) + v.preco_crianca * int(qnt_meia))
#             carrinho = Carrinho.objects.create(viagem=v, qnt_inteira=qnt_inteira, qnt_meia=qnt_meia, total=total)
#             carrinhoId = carrinho.pk
#             viagem_dic[v]=total
#             qnt_passagens=(int(qnt_inteira) + int(qnt_meia))
#             carrinhoDescricao = v.origem + '-' + v.destino
#             carrinhoAmount1 = v.preco_adulto
#             preco_pago = total
#             preco_original = v.preco_adulto * qnt_passagens
#             r = (preco_pago/preco_original) * 100
#             des = 100 - r
#             numero_decimal = '{:.2f}'.format(des)
#             print('preco-pago',preco_pago, 'preco-original',preco_original, 'desconto',numero_decimal)
#             #DISCOUNT_PERCENT=numero_decimal
#             
#             print(carrinhoId, total, carrinhoDescricao)
#             checkout = {
#                 'email':'rondynely@hotmail.com',
#                 'token':'9F7A75D37B074BF4812D45CA5091ABEC',
#                 'currency':'BRL',
#                 'itemId1':carrinhoId,
#                 'itemDescription1':'Manaus Anori',
#                 'itemAmount1':carrinhoAmount1,
#                 'itemQuantity1':qnt_passagens,
#                 'paymentMethodGroup1':'ONLINE_DEBIT',
#                 'paymentMethodConfigKey1_1':'DISCOUNT_PERCENT',
#                 'paymentMethodConfigValue1_1':numero_decimal
#                 }
#             
#             response = requests.post('https://ws.pagseguro.uol.com.br/v2/checkout',data=checkout)           
#             root = ET.fromstring(response.text)
#             code=root[0].text
#             carrinho_dic[carrinho]=code
#         
#         print(code_dic)  
#         
#         context= {'carrinho':carrinho_dic,
#                   'code':code_dic,
#                   'viagem':viagem_dic,
#                   'qnt_passagens':qnt_passagens}
#         
#         return render(request, 'dev_radioanori/lista-viagem-prototipo.html', context)
#===============================================================================

#===============================================================================
# def listar_viagens(request):
#     print("lista_viagens")
#     origem = request.POST.get('origem')  
#     qnt_inteira = request.POST.get('inteira') 
#     qnt_meia = request.POST.get('meia')
#     viagem_dic = {}
#     carrinho_dic = {}
#     code_dic = {}
#     qnt_passagens = []
#     if request.method=='POST':
#         print("POST")
#         viagem = Viagem.objects.filter(origem=origem)
#         
#         for v in viagem:
#             total=(v.preco_adulto * int(qnt_inteira) + v.preco_crianca * int(qnt_meia))
#             carrinho = Carrinho.objects.create(viagem=v, qnt_inteira=qnt_inteira, qnt_meia=qnt_meia, total=total)
#             carrinhoId = carrinho.pk
#             viagem_dic[v]=total
#             qnt_passagens=(int(qnt_inteira) + int(qnt_meia))
#             carrinhoDescricao = v.origem + '-' + v.destino
#             carrinhoAmount1 = v.preco_adulto
#             preco_pago = total
#             preco_original = v.preco_adulto * qnt_passagens
#             r = (preco_pago/preco_original) * 100
#             des = 100 - r
#             numero_decimal = '{:.2f}'.format(des)
#             
#             #DISCOUNT_PERCENT=numero_decimal
#             
#             print(carrinhoId, total, carrinhoDescricao)
#             sessions = {
#                 'email':'rondynely@hotmail.com',
#                 'token':'9F7A75D37B074BF4812D45CA5091ABEC',
#                 }
#             
#             response = requests.post('https://ws.pagseguro.uol.com.br/v2/sessions',data=sessions)           
#             root = ET.fromstring(response.text)
#             code=root[0].text
#             carrinho_dic[carrinho]=code
#           
#         
#         context= {'carrinho':carrinho_dic,
#                   'code':code_dic,
#                   'viagem':viagem_dic,
#                   'qnt_passagens':qnt_passagens}
#         
#         return render(request, 'dev_radioanori/lista-viagem-prototipo2.html', context)
#     
#===============================================================================


def listar_viagens(request):
    print("lista_viagens")
    origem = request.POST.get('origem')  
    qnt_inteira = request.POST.get('inteira') 
    qnt_meia = request.POST.get('meia')
    viagem_dic = {}
    carrinho_dic = {}
    code_dic = {}
    qnt_passagens = []
    if request.method=='POST':
        print("POST")
        viagem = Viagem.objects.filter(origem=origem)
        
        for v in viagem:
            total=(v.preco_adulto * int(qnt_inteira) + v.preco_crianca * int(qnt_meia))
            carrinho = Carrinho.objects.create(viagem=v, qnt_inteira=qnt_inteira, qnt_meia=qnt_meia, total=total)
            carrinhoId = carrinho.pk
            viagem_dic[v]=total
            qnt_passagens=(int(qnt_inteira) + int(qnt_meia))
            carrinhoDescricao = v.origem + '-' + v.destino
        
            carrinho_dic[carrinho] = qnt_passagens    
        print(carrinho_dic.items()) 
        
        context= {'carrinho':carrinho_dic,
                  'code':code_dic,
                  'viagem':viagem_dic,
                  'qnt_passagens':qnt_passagens}
        
        return render(request, 'dev_radioanori/lista-viagem-prototipo3.html', context)

def sandbox(request):
    print("sandbox")
    c = request.GET.get('pk', None)
    qnt = request.GET.get('qnt_passagens', None)
    carrinho = get_object_or_404(Carrinho, pk=c)
    car = carrinho.total
    car = '{:.2f}'.format(car)
    pagseguro_api = PagSeguroApiTransparent()
    data = pagseguro_api.get_session_id()
    session_id = data['session_id']
    
    if request.method=='POST':
        print("post")
        bandeira = request.POST.get('brand')
        nome = request.POST.get('username')
        token = request.POST.get('token')
        hashPagseguro = request.POST.get('hash')
        api = PagSeguroApiTransparent()
        descricao = carrinho.viagem.destino
        
        item1 = PagSeguroItem(id=c, description=descricao, amount=car, quantity=1)
        api.add_item(item1)
        
        sender = {'name': 'Jose Comprador', 'area_code': 92, 'phone': 56273440, 'email': 'comprador@uol.com.br', 'cpf': '22111944785',}
        api.set_sender(**sender)
        
        shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar', 'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA',}
        api.set_shipping(**shipping)
        
        api.set_payment_method('creditcard')
        data = {'quantity': 1, 'value': car, 'name': 'Jose Comprador', 'birth_date': '27/10/1987', 'cpf': '22111944785', 'area_code': 11, 'phone': 56273440, 'no_interest_quantity': 5}
        api.set_creditcard_data(**data)
        billing_address = {'street': 'Av. Brig. Faria Lima', 'number': 1384, 'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA',}
        api.set_creditcard_billing_address(**billing_address)
        api.set_creditcard_token(token)
        
        api.set_sender_hash(hashPagseguro)
        
        data = api.checkout()
        
        print("data", data)
        
        if data['success'] is False:
            raise CheckoutException(data['message'])
        
        print(notificacao_recebida.connect(load_signal)) 

        return HttpResponse(notificacao_recebida.connect(load_signal))
        
        
        
    context = {
        'session':session_id,
        'cart':carrinho,
        'qnt':qnt,
    
        }
    return render(request, 'dev_radioanori/sandbox-pagamento.html', context)

def sandbox_debito(request):
    if request.method=="POST":
        print("post/sandbox-debito")
        pk = request.POST.get('pk', None)
        carrinho = get_object_or_404(Carrinho, pk=pk)
        amount = carrinho.total
        amount = '{:.2f}'.format(amount)
        nome = request.POST.get('username')
        cpf = request.POST.get('cpf')
        brand = request.POST.get('brand_radio')
        hashPagseguro = request.POST.get('hash')
        qnt = carrinho.qnt_inteira + carrinho.qnt_meia
        descricao = "beiraonline " + carrinho.viagem.origem + "-" + carrinho.viagem.destino
        
        print('brand:',brand)
        print('nome:',nome)
        print('cpf',cpf)
        
        item1 = PagSeguroItem(id=pk, description=descricao, amount=amount, quantity=qnt)
        
        api = PagSeguroApiTransparent()
        api.add_item(item1)
        
        sender = {'name': nome, 'area_code': 92, 'phone': 56273440, 'email': 'comprador@uol.com.br', 'cpf': '22111944785',}
        api.set_sender(**sender)
        
        shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar', 'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP', 'country': 'BRA',}
        api.set_shipping(**shipping)
        
        api.set_payment_method('eft')
        api.set_bank_name('itau')
        
        api.set_sender_hash(hashPagseguro)
        
        data = api.checkout()
        
        #print("data", data)
        
        if data['success'] is False:
            raise CheckoutException(data['message'])
        
        payment_url = data['transaction']['paymentLink']

        return redirect(payment_url)
  
    return HttpResponse("deu certo")

def sandbox_checkbox(request):
    return render(request, 'dev_radioanori/sandbox-checkbox.html')

def load_signal(sender, transaction, **kwargs):
    print("load_signal")
    print(transaction['status'])
    return HttpResponse(transaction['status'])

def sandbox_checkout_realizado(request):
    resposta = checkout_realizado.connect(load_signal)
    print("checkout resposta", resposta)
    return HttpResponse(resposta)
   
    
def sandbox_pagamento(request):
    print('sandbox_pagamento')
    
    if request.method=="POST":
        print("post")
        pagseguro_api = PagSeguroApiTransparent()
        
        #json = serializers.serialize('json', session_id)
        return HttpResponse(json, content_type='application/json')
        
    
    return render(request, 'dev_radioanori/sandbox.html')

def sandbox_inicio_pagseguro(request):
    
    if request.method=="POST":
        print('sandboc-inicio-pagamento')
        pagseguro_api = PagSeguroApiTransparent()
        data = pagseguro_api.get_session_id()
        session_id = data['session_id']
        return JsonResponse(session_id)
            
def pagseguroAPI_transparente(request, pk):
    print("pagseguroAPI_transparente")
    session = request.GET.get('session')
    id = request.GET.get('pk')
    description = request.GET.get('pk')
    api = PagSeguroApiTransparent()
    item1 = PagSeguroItem(id=id, description='passagem', amount='200.00', quantity=1)
    api.add_item(item1)
    
    api.set_payment_method('eft')
    
    api.set_bank_name('itau')
    
    if request.method=="GET":
        context = {'session':session,
                   'item':item1}
        
        return render(request, 'dev_radioanori/pagseguro_transparente.html', context)
    
def carrinho(request):
    print("carrinho")
    origem = request.POST.get('origem')
    destino = request.POST.get('destino')
    data_viagem = request.POST.get('data_viagem')
    inteira = request.POST.get('inteira')
    meia = request.POST.get('meia')
    total = request.POST.get('total')
    total = float(total.replace(",","."))
    pk = request.POST.get('pk')
    qnt_passagens = int(inteira) + int(meia)
    
    
    if request.method=="POST":
        print("carrinho/POST")
        print('total:',total, 'pk:',pk)
      
        v = get_object_or_404(Viagem, pk=pk)
        carrinho = Carrinho.objects.create(viagem=v, qnt_inteira=inteira, qnt_meia=meia, total=total)
        
        #return redirect('pagseguroAPI', pk=carrinho.pk)
    
        return render(request, 'dev_radioanori/carrinho.html',{'pk':pk, 'origem':origem, 'destino':destino, 'inteira':inteira, 
                                                                'meia':meia,'qnt':qnt_passagens, 'total':total, 'carrinho':carrinho})

def pagseguro_transparente(request, code):
    print("pagseguro transparente")
    print(code)
    context = {
        'code':code
        }
    return render(request, 'dev_radioanori/pagseguro_transparente.html', context)


def pagseguroAPI(request, pk):
    print("pagseguro")
    
    carrinho = get_object_or_404(Carrinho, pk=pk)
    carrinhoId = carrinho.pk
    total = carrinho.total
    qnt_passagens = (carrinho.qnt_inteira + carrinho.qnt_meia)
    
    #===========================================================================
    # carrinhoCheckout = {
    #     'email':'rondynely@hotmail.com',
    #     'token':'9F7A75D37B074BF4812D45CA5091ABEC'
    #     
    #     }
    #===========================================================================

    if request.method=="POST":
        response = requests.post('https://ws.pagseguro.uol.com.br/v2/checkout?email=rondynely@hotmail.com&token=9F7A75D37B074BF4812D45CA5091ABEC&currency=BRL&itemId1=199&itemDescription1=Manaus-Anori&itemAmount1=250.00&itemQuantity1=1')           
        root = ET.fromstring(response.text)
        code=root[0].text
        
        return render(request, 'dev_radioanori/pagseguro-sandbox.html', {'code':code})
    
def testeAPI(request):
    response = requests.get('https://ws.pagseguro.uol.com.br/v2/checkout')
    json = response.json()
    list = []
    for js in json:
        list.append(js)
    
    return render(request, 'dev_radioanori/pagseguro-sandbox.html', {'list':list})

def carrinho_detalhe(request, pk):
    print("carrinho_detalhe")
    carrinho_detalhe = get_object_or_404(Carrinho, pk=pk)
    return render(request, 'dev_radioanori/carrinho_detalhe.html', {'carrinho_detalhe':carrinho_detalhe})

def escolher_poltrona(request, pk):
    carrinho = get_object_or_404(Carrinho, pk=pk)
    print('pk_carrinho:',carrinho.pk)
    cart_total = carrinho.total
    qnt = request.GET.get('qnt_passagens')
    qnt = int(qnt)
    pk_poltrona=Poltrona.objects.get(viagem=carrinho.viagem.pk)
    pk_pol=pk_poltrona.pk
    num_pol = []
    np=[]
    
    if request.method=="POST":
        num_usuario = request.POST.getlist('pesquisa')
        name = request.POST.getlist('username')
        cpf = request.POST.getlist('cpf')
        
        for p, n, c in zip(num_usuario, name, cpf):
            Passagem.objects.create(poltrona=p, carrinho=carrinho, nome_passageiro=n, cpf=c)
            num_pol.append(int(p))
        
        print('poltronas do usuario:',num_pol)
        
        p = Poltrona.objects.get(viagem=carrinho.viagem.pk)
        pk_pol=p.pk
        print('indisponiveis antes:',p.poltronas_indisponiveis)
        np = p.poltronas_indisponiveis
        np =np.strip('[]').strip('"''"')
        print(np)
        b = ","
        for i in range(0,len(b)):
            np=np.replace(b[i],"")
            np=np.split()
        print(np)
        np = [int(i) for i in np]
        print('np',np)
        for n in num_pol:    
            np.append(n)
        print('num_pol final',num_pol)
        print('np_final', np)
        p.poltronas_indisponiveis = np
        p.save()
            
        p = Poltrona.objects.get(pk=pk_pol)
        print('indisponiveis depois',p.poltronas_indisponiveis)
        
        return redirect('fechar-venda', pk=carrinho.pk)
        
    context = {
        'qnt':range(1, (qnt + 1) ),
        'total':cart_total,
        'pk_pol':pk_pol
        }
        

    
    return render(request, 'dev_radioanori/mapa-poltrona.html', context)

def fechar_venda(request, pk):
    cart = get_object_or_404(Carrinho, pk=pk)
    nome = []
    for x in Passagem.objects.filter(carrinho=cart):
        nome.append(x.nome_passageiro)
        print(x.nome_passageiro)
    
    return HttpResponse("Venda fechada, Compartilhe sua Chegada:")
    

def pesquisar_poltronas(request):
    pk=request.GET.get('pk_poltrona')
    print('pk',pk)
    poltronas = Poltrona.objects.get(pk=pk)
    
    data = {
        'poltronas': poltronas.poltronas_indisponiveis
    }
    print('lista poltrona',poltronas.poltronas_indisponiveis)
    
    return JsonResponse(data)
    
    
    
    
#===============================================================================
# API Pagseguro
#===============================================================================


#===============================================================================
# def viagem_list(request):
#     print("viagem_list")
#     origem = request.POST.get('origem')  
#     qnt_inteira = int(request.POST.get('inteira')) 
#     qnt_meia = int(request.POST.get('meia'))
#     viagens = {}
#     total = []
#     lista1 = []
#     lista2 = []
#     lista =[]
#     if request.method=='POST':
#         print("POST")
#         viagem = Viagem.objects.filter(origem=origem)
#         #cart = Cart.objects.get_cart_for_user(request.user)
#         for v in viagem:
#             ticket1 = Ticket.objects.create(viagem = v, title="Inteira para " + v.destino, type=1, price=v.preco_adulto)
#             ticket2 = Ticket.objects.create(viagem = v, title="Meia para " + v.destino, type=2, price=v.preco_crianca)
#             lista1 = [ticket1 for x in list(range(qnt_inteira))]
#             lista1.append([ticket2 for x in list(range(qnt_meia))])    
#             #total.append(qnt_inteira * v.preco_adulto + qnt_meia * v.preco_crianca)
#                   
#         for l in lista1[qnt_inteira]:
#             if l:
#                 lista.append(l)
#             else:
#                 print('vazia',l)     
#         for l1 in lista1[:qnt_inteira]:
#             print(l1.type)
#             lista.append(l1)
#         
#         for l2 in lista:
#             print('tipo:', l2.type)
#         
#         for v in viagem:
#             viagens[v]=lista.__str__()
#         
#         context = {
#             'lista':lista1,
#             'quantity':(int(qnt_inteira) + int(qnt_meia)),
#             'viagem':viagens
#             }
#         return render(request, 'dev_radioanori/lista-viagem-prototipo3.html', context=context)
# 
# 
# def event_detail(request, pk):
#     event = get_object_or_404(Viagem, id=pk)
#     context = {
#         'event': event,
#         'cart': Cart.objects.get_cart_for_user(request.user)
#     }
#     return render(request, 'tickets/event_detail.html', context=context)
# 
# def cart_detail(request):
#     context = {
#         'cart': Cart.objects.get_cart_for_user(request.user)
#     }
#     return render(request, 'dev_radioanori/cart-detail.html', context=context)
# 
# 
# 
# @require_http_methods(['POST'])
# def cart_clear(request):
#     cart = Cart.objects.get_cart_for_user(request.user)
#     cart.cart_items.all().delete()
#     return redirect('cart_detail')
# 
# 
# 
# @require_http_methods(['POST'])
# def cart_add_item(request):
#     print("cart_add_item")
#     cart = Cart.objects.get_cart_for_user(request.user)
#     tickets = request.POST.get('tickets')
#     
#     if request.method=="POST":
#         #print("cart_item_POST")
#         #if form.is_valid():
#         print(tickets)
#         for t in tickets:
#             Cart.objects.add_cart_item(cart.pk, t, 1)
#         
#         return redirect('cart_detail')
# 
# 
# 
# @require_http_methods(['POST'])
# @transaction.atomic
# def purchase_create(request):
#     cart = Cart.objects.get_cart_for_user(request.user)
#     purchase = Purchase.objects.create_checkout(cart)
#     print(purchase.pk)
#     return redirect('purchase_detail', pk=purchase.pk)
# 
# 
# 
# def purchase_list(request):
#     purchases = Purchase.objects.filter(user=request.user)
#     context = {'purchases': purchases}
#     return render(request, 'tickets/purchase_list.html', context=context)
# 
# 
# 
# def purchase_detail(request, pk):
#     purchase = get_object_or_404(Purchase, id=pk, user=request.user)
#     context = {'purchase': purchase}
#     return render(request, 'tickets/purchase_detail.html', context=context)
#===============================================================================
