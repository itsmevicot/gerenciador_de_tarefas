from ckeditor.widgets import CKEditorWidget
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from django.contrib.auth.hashers import check_password

from gerenciamento.models import Usuario, Tarefa, TipoTarefa, PrioridadeTarefa, ObservacaoTarefa, SituacaoTarefa


class CadastroForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, required=False)
    email = forms.EmailField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=16, min_length=8, widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(label='Confirmação de Senha', max_length=16, min_length=8, widget=forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("nome",css_class="form-group col-12 col-md-10"),
                Column("email", css_class="form-group col-12 col-md-10"),
                Column("senha", css_class="form-group col-12 col-md-10"),
                Column("confirmar_senha", css_class="form-group col-12 col-md-10"),
            ),
            Submit('submit', 'Cadastrar', css_class='btn-primary'))


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("O email inserido já é cadastrado.")
        return email

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise forms.ValidationError("As senhas não são iguais.")
        return confirmar_senha


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', max_length=16, min_length=8, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("email", css_class="form-group col-12 col-md-10"),
                Column("senha", css_class="form-group col-12 col-md-10"),
            ),
            Submit('submit', 'Acessar o sistema', css_class='btn-primary'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            raise forms.ValidationError("O email deve ser preenchido.")
        if not Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse email não está cadastrado.")
        return email

    def clean(self):
        senha = self.cleaned_data.get('senha')
        email = self.cleaned_data.get('email')
        usuario = Usuario.objects.filter(email=email).first()
        if usuario is None:
            raise forms.ValidationError("O email não está cadastrado!")

        senha_banco = usuario.password

        if not check_password(senha, senha_banco):
            raise forms.ValidationError("A senha está incorreta!")
        if senha == "":
            raise forms.ValidationError("A senha deve ser preenchida.")

class AdicionarTarefaForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=[(None, 'Selecione um tipo')] + list(TipoTarefa.CHOICES), label='Tipo', required=True)
    prioridade = forms.ChoiceField(choices=[(None, 'Selecione uma prioridade')] + list(PrioridadeTarefa.CHOICES), label='Prioridade', required=True)
    class Meta:
        model = Tarefa
        fields = ('titulo', 'tipo', 'prioridade', 'descricao')


class AdicionarObservacaoForm(forms.ModelForm):
    class Meta:
        model = ObservacaoTarefa
        fields = ('observacao',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['observacao'].label= "Nova observação"
        self.fields['observacao'].widget = CKEditorWidget()

        self.helper.layout = Layout(
            Field('observacao', css_class='ckeditor')
        )