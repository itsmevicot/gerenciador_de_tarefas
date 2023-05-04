from django.urls import path
from . import views

urlpatterns = [
    # Login, Cadastro e Logout
    path('', views.login, name='login'),
    path('cadastro/', views.realizar_cadastro, name='realizar_cadastro'),
    path('logout/', views.logout_user, name='logout'),

    # Tarefas
    path('adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),
    path('listar_tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('detalhar_tarefa/<id_tarefa>/', views.detalhar_tarefa, name='detalhar_tarefa'),
    path('assumir_tarefa/<id_tarefa>', views.assumir_tarefa, name='assumir_tarefa'),
    path('finalizar_tarefa/<id_tarefa>', views.finalizar_tarefa, name='finalizar_tarefa'),

    # Observações
    path('adicionar_observacao/<id_tarefa>', views.adicionar_observacao, name='adicionar_observacao'),
    path('editar_ultima_observacao/<id_tarefa>', views.editar_ultima_observacao, name='editar_ultima_observacao'),
]
