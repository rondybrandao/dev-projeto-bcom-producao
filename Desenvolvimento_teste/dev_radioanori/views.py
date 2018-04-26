from django.shortcuts import render, redirect, get_object_or_404
from .models import Viagem, Compra, Carrinho
from dev_radioanori.models import Passagem
from django.template.context_processors import request
from django.http.response import HttpResponse
from xml.dom.minidom import parse

import xml.etree.ElementTree as ET
import requests
import decimal
from imaplib import Response_code


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
            print('preco-pago',preco_pago, 'preco-original',preco_original, 'desconto',numero_decimal)
            #DISCOUNT_PERCENT=numero_decimal
            
            print(carrinhoId, total, carrinhoDescricao)
            checkout = {
                'email':'rondynely@hotmail.com',
                'token':'9F7A75D37B074BF4812D45CA5091ABEC',
                'currency':'BRL',
                'itemId1':carrinhoId,
                'itemDescription1':'Manaus Anori',
                'itemAmount1':carrinhoAmount1,
                'itemQuantity1':qnt_passagens,
                'paymentMethodGroup1':'ONLINE_DEBIT',
                'paymentMethodConfigKey1_1':'DISCOUNT_PERCENT',
                'paymentMethodConfigValue1_1':numero_decimal
                }
            
            response = requests.post('https://ws.pagseguro.uol.com.br/v2/checkout',data=checkout)           
            root = ET.fromstring(response.text)
            code=root[0].text
            carrinho_dic[carrinho]=code
        
        print(code_dic)  
        
        context= {'carrinho':carrinho_dic,
                  'code':code_dic,
                  'viagem':viagem_dic,
                  'qnt_passagens':qnt_passagens}
        
        return render(request, 'dev_radioanori/lista-viagem-prototipo.html', context)
             

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
    carrinho_detalhe = get_object_or_404(Carrinho, pk=pk)
    return render(request, 'dev_radioanori/carrinho_detalhe.html', {'carrinho_detalhe':carrinho_detalhe})

def escolher_poltrona(request, pk):
    carrinho = get_object_or_404(Carrinho, pk=pk)
    num_usuario = request.POST.getlist('pesquisa')
    print(num_usuario)
    if request.method=="POST":
        passagem = Passagem(poltrona=num_usuario,carrinho=carrinho)
        print(passagem.poltrona)
        
    
    return render(request, 'dev_radioanori/mapa-poltrona.html')



