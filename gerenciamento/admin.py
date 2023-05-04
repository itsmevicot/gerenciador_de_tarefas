from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from gerenciamento.models import Usuario, Tarefa, ObservacaoTarefa


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'nome')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    ordering = ('criado_em',)
    search_fields = ('email', 'nome')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'titulo', 'prioridade')
    list_filter = ('tipo', 'prioridade', 'situacao')
    search_fields = ('titulo',)

@admin.register(ObservacaoTarefa)
class ObservacaoTarefaAdmin(admin.ModelAdmin):
    list_display = ('tarefa', 'observacao')
    list_filter = ('tarefa',)
    search_fields = ('tarefa',)



admin.site.register(Usuario, UsuarioAdmin)
