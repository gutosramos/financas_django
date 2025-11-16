from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entrada/nova/', views.nova_entrada, name='nova_entrada'),
    path('saida/nova/', views.nova_saida, name='nova_saida'),
    # ROTAS DE EXCLUSÃO
    path('entrada/excluir/<int:id>/', views.excluir_entrada, name='excluir_entrada'),
    path('saida/excluir/<int:id>/', views.excluir_saida, name='excluir_saida'),

]
