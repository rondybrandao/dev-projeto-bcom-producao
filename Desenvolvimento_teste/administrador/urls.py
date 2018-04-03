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
    
    url(r'formulario-despesas', views.controle_despesas, name='form-despesas'),
    url(r'despesa_detail/(?P<pk>[0-9]+)$', views.despesa_detail, name='despesa-detail'),
    url(r'despesa_detail/(?P<pk>[0-9]+)/edit$', views.despesa_edit, name='despesa-edit'),
    
    url(r'tripulacao', views.tripulacao, name='tripulacao'),
    url(r'detail/(?P<pk>[0-9]+)$', views.confirmacao_tripulacao, name='tripulacao-detail'),
    url(r'detail/(?P<pk>[0-9]+)/edit$', views.tripulacao_edit, name='tripulacao-edit'),
    
    url(r'manutencao', views.manutencao, name='manutencao'),
    url(r'confirmacao/(?P<pk>[0-9]+)$', views.confirmacao_manutencao, name='mt'),
    url(r'confirmacao-edit/(?P<pk>[0-9]+)/edit$', views.manutencao_edit, name='manutencao-edit'),

    
    url(r'detalhe-da-receita/', views.detalhar_receita_admin, name='detalhar-receita'),
    url(r'detalhe-das-passagens/', views.detalhar_passagem_admin, name='detalhar-passagem'),
    url(r'detalhe-das-despesas/', views.detalhar_despesas_admin, name='detalhar-despesa'),
    url(r'detalhe-das-manutencoes/', views.detalhar_manutencoes_admin, name='detalhar-manutencao'),
    url(r'tabela-dos-tripulantes/', views.tables_tripulation, name='tables-tripulation'),
    

    url(r'formulario-google', views.form_google, name='form-google'),
    
    url(r'formulario-controle-step', views.controle_step, name='form-controle-step'),
    
    
]
