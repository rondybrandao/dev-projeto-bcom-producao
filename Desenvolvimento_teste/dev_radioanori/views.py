from django.shortcuts import render, redirect, get_object_or_404
from .models import Viagem, Compra, Carrinho

# Create your views here.

def index_old(request):
    return render(request, 'dev_radioanori/index.html')

def index(request):
    origem_entrada = request.POST.get('sel1')
    qnt_adulto = request.POST.get('adulto')
    qnt_crianca = request.POST.get('crianca')
    if request.method=='POST':
        viagem = Viagem.objects.filter(origem=origem_entrada)
        for v in viagem:
            passagem = Compra(viagem = v, qnt_adulto=qnt_adulto, qnt_crianca=qnt_crianca, nome_passageiro="rondy")
            passagem.save()
        return redirect('carrinho', pk=passagem.pk) 
        
    return render(request, 'dev_radioanori/index.html')

def carrinho(request, pk):
    passagem = get_object_or_404(Compra, pk=pk)
    total = (int(passagem.qnt_adulto) * passagem.viagem.preco_adulto) + (int(passagem.qnt_crianca) * passagem.viagem.preco_crianca)
    
    if request.method=='POST':
        carrinho = Carrinho(compra=passagem, total=total)
        carrinho.save()
        print(request)
        return redirect('carrinho_detalhe', pk=carrinho.pk)
        
    else:
        if request.method=='GET':
            nova_origem = request.GET.get('sel1')
            print(nova_origem)
            try:
                viagem = Viagem.objects.filter(origem=nova_origem)
                for v in viagem:
                    passagem = Compra.objects.filter(pk=pk).update(viagem=v.pk)
                    passagem = get_object_or_404(Compra, pk=pk)
                    passagem.save()
                return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
                                                                'total': total})
            except Viagem.DoesNotExist:
                pass 
                
    return render(request, 'dev_radioanori/lista_viagem.html', {'passagem':passagem,
                                                                'total': total})

def carrinho_detalhe(request, pk):
    carrinho_detalhe = get_object_or_404(Carrinho, pk=pk)
    return render(request, 'dev_radioanori/carrinho_detalhe.html', {'carrinho_detalhe':carrinho_detalhe})


