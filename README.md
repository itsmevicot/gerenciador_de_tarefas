# Gerenciador de tarefas criado para um processo seletivo

### Para rodar o projeto em ambiente Windows:

1. Crie um ambiente virtual com o comando: `python -m venv venv`
2. Ative o ambiente virtual com o comando: `venv\Scripts\activate`
3. Instale as dependências com o comando: `pip install -r requirements.txt`
4. Altere em `gerenciamento => settings.py` as configurações de banco de dados para o seu ambiente local
5. Rode o projeto com o comando: `python manage.py runserver`
6. Atualize o banco de dados com o comando: `python manage.py migrate`
7. Tudo pronto! Basta utilizar a aplicação.

### Funções implementadas
- Cadastro de usuário
- Login
- Logout
- Adicionar tarefa
- Listagem de tarefas
- Detalhamento de tarefa
- Adicionar observação
- Editar ultima observação
- Assumir a responsabilidade de uma tarefa
- Finalizar uma tarefa

### Funções a serem implementadas
1. Filtro de tarefas
2. Conteinerização com Docker
3. Mudar nome e senha de usuário
4. Implementar cadastro por verificação de email
5. Implementação de testes unitários


### Frameworks e bibliotecas
- Construído com Python/Django, HTML, CSS e JavaScript 
- Django Crispy para formulários
- Django CKEditor para implementação do RichTextField
- Bootstrap para estilização

### Requisitos necessários
- Necessário a criação de um servidor no PostgreSQL com o nome de `gerenciamento` ou alteração no arquivo settings.py para o novo nome. Recomendo uso do pgAdmin4 como SGBD (Sistema de Gerenciamento de Banco de Dados)
