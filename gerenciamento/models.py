from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from ckeditor.fields import RichTextField

class UserManager(BaseUserManager):
    use_in_migrations = False

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Informe um email válido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um superusuário deve ter o atributo is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Um superusuário deve ter o atributo is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, unique=True, default='')
    nome = models.CharField(max_length=255, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.nome if self.nome else self.email


    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


    def get_full_name(self):
        return self.nome


    def get_short_name(self):
        return self.nome or self.email.split('@')[0]


class PrioridadeTarefa:
    SEM_PRIORIDADE = '0'
    BAIXA = '1'
    MEDIA = '2'
    ALTA = '3'

    CHOICES = (
        (SEM_PRIORIDADE, 'Sem prioridade'),
        (BAIXA, 'Baixa'),
        (MEDIA, 'Média'),
        (ALTA, 'Alta'),
    )


class TipoTarefa:
    INCIDENTE = '0'
    SOLICITACAO_SERVICO = '1'
    MELHORIAS = '2'
    PROJETOS = '3'

    CHOICES = (
        (INCIDENTE, 'Incidente'),
        (SOLICITACAO_SERVICO, 'Solicitação de serviço'),
        (MELHORIAS, 'Melhorias'),
        (PROJETOS, 'Projetos'),
    )


class SituacaoTarefa: # Não há nos requisitos funcionais nenhum detalhe sobre as opções de situação de uma tarefa
    ABERTA = '0'
    CONCLUIDA = '1'

    CHOICES = (
        (ABERTA, 'Aberta'),
        (CONCLUIDA, 'Concluída'),
    )

class Tarefa(models.Model):
    titulo = models.CharField('Título', max_length=255)
    descricao = RichTextField('Descrição')
    tipo = models.CharField('Tipo', max_length=1, choices=TipoTarefa.CHOICES)
    prioridade = models.CharField('Prioridade', max_length=1, choices=PrioridadeTarefa.CHOICES)
    responsavel_tarefa = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='responsavel_tarefa')
    situacao = models.CharField('Situação', max_length=1, choices=SituacaoTarefa.CHOICES, default=SituacaoTarefa.ABERTA)
    data_abertura = models.DateTimeField('Data de abertura', auto_now_add=True)
    data_conclusao = models.DateTimeField('Data de conclusão', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.titulo

    def get_custom_id(self):
        return f"{str(self.id).zfill(4)}"

    def get_tipo(self):
        return self.get_tipo_display()

    def get_prioridade(self):
        return self.get_prioridade_display()

    @property
    def is_responsable(self):
        return self.responsavel_tarefa == self.request.user

    @property
    def pode_finalizar_tarefa(self):
        return self.situacao != SituacaoTarefa.CONCLUIDA

    @property
    def pode_adicionar_observacao(self):
        return True if self.responsavel_tarefa == self.request.user and self.tarefa.situacao != SituacaoTarefa.CONCLUIDA else False




class ObservacaoTarefa(models.Model):
    observacao = RichTextField('Observação', null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='observacoes')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.observacao

    @property
    def ultima_observacao(self):
        return ObservacaoTarefa.objects.filter(tarefa=self.tarefa).order_by('-criado_em').first()
