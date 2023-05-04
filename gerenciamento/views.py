from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from gerenciamento.forms import CadastroForm, LoginForm, AdicionarTarefaForm, AdicionarObservacaoForm
from gerenciamento.models import Usuario, Tarefa, SituacaoTarefa, ObservacaoTarefa
from django.contrib import auth, messages
from datetime import datetime



def realizar_cadastro(request):
    ''' View para realizar o cadastro de um usuário na plataforma. '''

    form = CadastroForm(request.POST or None)
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            nome = form.cleaned_data['nome']
            Usuario.objects._create_user(email=email, password=senha, nome=nome)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('login')

    return render(request,'cadastro.html', locals())


def login(request):
    ''' View para realizar o login na plataforma.'''

    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            user = auth.authenticate(username=email, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('listar_tarefas')
    return render(request, 'login.html', locals())


@login_required
def logout_user(request):
    ''' View para realizar o logout na plataforma.'''

    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')


@login_required
def adicionar_tarefa(request):
    ''' View para adicionar uma tarefa na plataforma.'''

    form = AdicionarTarefaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                tarefa = form.save(commit=False)
                tarefa.responsavel_tarefa = request.user
                tarefa.save()
                messages.success(request, f"Tarefa #{tarefa.get_custom_id()}  adicionada com sucesso!")
                return redirect('listar_tarefas')
    return render(request, 'usuarios/adicionar_tarefa.html', locals())


@login_required
def listar_tarefas(request):
    ''' View para fazer a listagem de todas as tarefas e das tarefas do usuário.'''
    tarefas = Tarefa.objects.exclude(situacao=SituacaoTarefa.CONCLUIDA).order_by('id')
    tarefas_usuario = Tarefa.objects.filter(responsavel_tarefa=request.user).exclude(situacao=SituacaoTarefa.CONCLUIDA)
    paginator = Paginator(tarefas, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'usuarios/listar_tarefas.html', locals())


@login_required
def detalhar_tarefa(request, id_tarefa):
    ''' View para realizar o detalhamento da tarefa.
    :params: id_tarefa: id da tarefa que será detalhada.'''
    tarefa = get_object_or_404(Tarefa, pk=id_tarefa)
    form_adicionar_observacao = AdicionarObservacaoForm(request.POST or None)
    form_descricao_preenchida = AdicionarTarefaForm(request.POST or None, instance=tarefa)
    pode_assumir_tarefa = True if tarefa.responsavel_tarefa != request.user else False
    pode_finalizar_tarefa = True if tarefa.responsavel_tarefa == request.user\
                                    and tarefa.situacao != SituacaoTarefa.CONCLUIDA else False
    ultima_observacao = tarefa.observacoes.last().pk if tarefa.observacoes.last() else None
    pode_adicionar_observacao = True if request.user == tarefa.responsavel_tarefa else False
    observacoes = tarefa.observacoes.all().order_by('-criado_em')
    if tarefa.observacoes.last():
        pode_editar_observacao = True if tarefa.observacoes.last().usuario.pk == request.user.pk\
                                         and tarefa.situacao != SituacaoTarefa.CONCLUIDA else False
    return render(request, 'usuarios/detalhar_tarefa.html', locals())


@login_required
def adicionar_observacao(request, id_tarefa):
    ''' View para adicionar uma observação a uma tarefa.'''
    tarefa = get_object_or_404(Tarefa, pk=id_tarefa)
    form = AdicionarObservacaoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                observacao = form.save(commit=False)
                observacao.tarefa = tarefa
                observacao.usuario = request.user
                observacao.save()
                messages.success(request, "Observação adicionada com sucesso!")
                return redirect('listar_tarefas')
    return render(request, 'usuarios/adicionar_observacao.html', locals())


@login_required
def editar_ultima_observacao(request, id_tarefa):
    ''' View para editar a ultima observação de uma tarefa.'''
    tarefa = get_object_or_404(Tarefa, pk=id_tarefa)
    ultima_observacao = tarefa.observacoes.all().order_by('-criado_em').first()
    form = AdicionarObservacaoForm(request.POST or None, instance=ultima_observacao)
    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                observacao = ObservacaoTarefa.objects.get(pk=ultima_observacao.pk)
                observacao.observacao = form.cleaned_data['observacao']
                observacao.save()
                messages.success(request, "Observação editada com sucesso!")
                return redirect('listar_tarefas')
    return render(request, 'usuarios/editar_ultima_observacao.html', locals())

@login_required
def assumir_tarefa(request, id_tarefa):
    ''' View para assumir a responsabilidade de uma tarefa. '''
    tarefa = get_object_or_404(Tarefa, pk=id_tarefa)
    tarefa.responsavel_tarefa = request.user
    tarefa.save()
    messages.success(request, "Tarefa assumida com sucesso!")
    return redirect('listar_tarefas')


@login_required
def finalizar_tarefa(request, id_tarefa):
    ''' View para finalizar uma tarefa. Altera o status da tarefa para CONCLUIDA.'''
    tarefa = get_object_or_404(Tarefa, pk=id_tarefa)
    form_adicionar_conclusao = AdicionarObservacaoForm(request.POST or None)
    if form_adicionar_conclusao.is_valid():
        with transaction.atomic():
            observacao = form_adicionar_conclusao.save(commit=False)
            observacao.tarefa = tarefa
            observacao.usuario = request.user
            observacao.save()
            tarefa.data_conclusao = datetime.now()
            tarefa.situacao = SituacaoTarefa.CONCLUIDA
            tarefa.save()
            messages.success(request, "Tarefa finalizada com sucesso!")
        return redirect('listar_tarefas')
    return render(request, 'usuarios/finalizar_tarefa.html', locals())
