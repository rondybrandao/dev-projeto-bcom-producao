'''
Created on 26 de out de 2017

@author: rondy
'''

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index-home'),
    #url(r'^passagens/$', views.passagem, name='passagem'),
    #url(r'^lista_carrinho/(?P<pk>[0-9]+)/$', views.carrinho, name='carrinho'),
    url(r'^pesquisar-viagens/$', views.pesquisar_viagens, name='pesquisar'),
    url(r'^listar-viagens/$', views.listar_viagens, name='lista-viagem'),
    
    url(r'^pesquisar-viagens/carrinho/$', views.carrinho, name='carrinho'),
    url(r'^carrinho_detalhe/(?P<pk>[0-9]+)/$', views.carrinho_detalhe, name='carrinho_detalhe'),
    
    
    
    url(r'^pagseguroAPI/(?P<pk>[0-9]+)/$', views.pagseguroAPI, name='pagseguroAPI'),
    url(r'^pagseguroAPI_transparente/(?P<pk>[0-9]+)/$', views.pagseguroAPI_transparente, name='pagseguro-transparente'),
    url(r'^testeAPI/$', views.testeAPI, name='testeAPI'),
    
    url(r'^sandbox/$', views.sandbox, name='sandbox'),
    url(r'^sandbox-pagamento/$', views.sandbox_pagamento, name='sandbox-pagamento'),
    url(r'^sandbox-inicio-pagamento/$', views.sandbox_inicio_pagseguro, name='inicio-pagseguro'),
    url(r'^sandbox-debito/$', views.sandbox_debito, name='sandbox-debito'),
    url(r'^sandbox-checkout-realizado/$', views.sandbox_checkout_realizado, name='checkout-realizado'),
    url(r'^sandbox-checkbox/$', views.sandbox_checkbox, name='sandbox-checkbox'),
    
    #url(r'^viagens-list/$', views.viagem_list, name='viagem-list'),
    #url(r'^viagens-list/carrinho/$', views.cart_detail, name='cart_detail'),
    #url(r'^viagens-list/adicionar/$', views.cart_add_item, name='cart_add_item'),
    
    url(r'^escolher-poltrona/(?P<pk>[0-9]+)/$', views.escolher_poltrona, name='escolher-poltrona'),
    url(r'^fechar-venda/(?P<pk>[0-9]+)/$', views.fechar_venda, name='fechar-venda'),
    url(r'^pesquisar-poltronas/', views.pesquisar_poltronas, name='pesquisar-poltronas'),
    
    url(r'^retorno/pagseguro/', include('pagseguro.urls')),
]
