'''
Created on 12 de nov de 2017

@author: rondy
'''

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'index', views.index),
    url(r'charts', views.charts, name='charts'),
    url(r'api/graphic', views.get_data, name='api-data'),
    url(r'api/data/graphic', views.ChartLineData.as_view()),
    url(r'tables', views.tables, name='tables'),   
    url(r'formulario-controle', views.controle, name='form-controle'),
    url(r'formulario-receita/(?P<pk>[0-9]+)$', views.receita_detail, name='receita-detail'),
    url(r'formulario-receita/(?P<pk>[0-9]+)/edit$', views.receita_edit, name='receita-edit'),
    
    url(r'formulario-despesas', views.controle_despesas, name='form-despesas'),
    url(r'despesa_detail/(?P<pk>[0-9]+)$', views.despesa_detail, name='despesa-detail'),
    url(r'despesa_detail/(?P<pk>[0-9]+)/edit$', views.despesa_edit, name='despesa-edit'),
    
    #url(r'formulario-controle/confirmacao', views.confirmacao_controle, name='form-controle'),
    #url(r'formulario-controle/(?P<pk_receita>[0-9]+)/(?P<pk_despesas>[0-9]+)$', views.confirmacao_controle, name='confirmacao_controle'),
    
    #url(r'form-controle', views.controle),
    url(r'formulario-google', views.form_google, name='form-google'),
    url(r'manutencao-registrar', views.manutencao_registrar, name='manutencao-registrar'),
    url(r'tripulacao-registrar', views.tripulacao_registrar, name='tripulacao-registrar'),
    
    url(r'formulario-controle-step', views.controle_step, name='form-controle-step'),
    
    url(r'manutencao', views.prototipo_manutencao, name='prototipo'),
]
