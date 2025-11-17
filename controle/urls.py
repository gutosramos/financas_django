from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Criar
    path('entrada/nova/', views.nova_entrada, name='nova_entrada'),
    path('saida/nova/', views.nova_saida, name='nova_saida'),
    path('reserva/nova/', views.nova_reserva, name='nova_reserva'),

    # Excluir
    path('entrada/excluir/<int:id>/', views.excluir_entrada, name='excluir_entrada'),
    path('saida/excluir/<int:id>/', views.excluir_saida, name='excluir_saida'),
    path('reserva/excluir/<int:id>/', views.excluir_reserva, name='excluir_reserva'),
]
