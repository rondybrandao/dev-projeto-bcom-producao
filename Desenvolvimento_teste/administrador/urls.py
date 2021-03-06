'''
Created on 12 de nov de 2017

@author: rondy
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'index', views.index, name='index'),
    
    url(r'api/data/graphic', views.ChartLineData.as_view()),
    
    url(r'formulario-controle', views.controle, name='form-controle'),
    url(r'formulario-receita/(?P<pk>[0-9]+)$', views.receita_detail, name='receita-detail'),
    url(r'formulario-receita/(?P<pk>[0-9]+)/edit$', views.receita_edit, name='receita-edit'),
    url(r'lista-das-receitas/$', views.receita_list, name='receita-list'),
    url(r'confirmacao-da-receita/$', views.receita_confirmacao, name='receita-confirmacao'),
    url(r'delete-item/(?P<pk>[0-9]+)/delete$', views.receita_delete, name='receita-delete'),
    
    url(r'formulario-despesas', views.controle_despesas, name='form-despesas'),
    url(r'despesa_detail/(?P<pk>[0-9]+)$', views.despesa_detail, name='despesa-detail'),
    url(r'despesa_detail/(?P<pk>[0-9]+)/edit$', views.despesa_edit, name='despesa-edit'),
    url(r'lista-das-despesas/$', views.despesa_list, name='despesa-list'),
    url(r'delete-despesa/(?P<pk>[0-9]+)/delete$', views.despesa_delete, name='despesa-delete'),
    
    url(r'tripulacao', views.tripulacao, name='tripulacao'),
    url(r'detail/(?P<pk>[0-9]+)$', views.confirmacao_tripulacao, name='tripulacao-detail'),
    url(r'detail/(?P<pk>[0-9]+)/edit$', views.tripulacao_edit, name='tripulacao-edit'),
    url(r'lista-dos-tripulantes/', views.tripulacao_list, name='tripulacao-list'),
    url(r'descricao-do-tripulante/(?P<pk>[0-9]+)$', views.tripulacao_descricao, name='tripulacao-descricao'),
    url(r'delete/(?P<pk>[0-9]+)/delete$', views.tripulacao_delete, name='tripulacao-delete'),
    
    url(r'manutencao', views.manutencao, name='manutencao'),
    url(r'confirmacao/(?P<pk>[0-9]+)$', views.confirmacao_manutencao, name='mt'),
    url(r'confirmacao-edit/(?P<pk>[0-9]+)/edit$', views.manutencao_edit, name='manutencao-edit'),
    url(r'descricao-das-manutencoes/(?P<pk>[0-9]+)$', views.manutencao_descricao, name='manutencao-descricao'),
    url(r'item-das-manutencoes/(?P<pk>[0-9]+)$', views.manutencao_item, name='manutencao-item'),
    url(r'lista-das-manutencoes/', views.manutencao_list, name='manutencao-list'),
    url(r'delete-(?P<pk>[0-9]+)/delete$', views.manutencao_delete, name='manutencao-delete'),

    
    url(r'detalhe-da-receita/', views.detalhar_receita_admin, name='detalhar-receita'),
    url(r'detalhe-das-passagens/', views.detalhar_passagem_admin, name='detalhar-passagem'),
    url(r'detalhe-das-despesas/', views.detalhar_despesas_admin, name='detalhar-despesa'),
    url(r'detalhe-das-manutencoes/', views.detalhar_manutencoes_admin, name='detalhar-manutencao'),
    url(r'tabela-dos-tripulantes/', views.tables_tripulation, name='tables-tripulation'),
    
    url(r'bug/', views.bug, name='bug'),

    url(r'formulario-google', views.form_google, name='form-google'),
    
    url(r'formulario-controle-step', views.controle_step, name='form-controle-step'),
    
    
]
