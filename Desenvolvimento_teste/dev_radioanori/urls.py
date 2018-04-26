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
    url(r'^pesquisar-viagens/carrinho/$', views.carrinho, name='carrinho'),
    url(r'^carrinho_detalhe/(?P<pk>[0-9]+)/$', views.carrinho_detalhe, name='carrinho_detalhe'),
    url(r'^escolher-poltrona/(?P<pk>[0-9]+)/$', views.escolher_poltrona, name='escolher-poltrona'),
     url(r'^pagseguroAPI/(?P<pk>[0-9]+)/$', views.pagseguroAPI, name='pagseguroAPI'),
    url(r'^testeAPI/$', views.testeAPI, name='testeAPI'),
    
]
