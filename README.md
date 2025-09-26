# Video Display Cycler - Guia de Execução no Linux com Docker

Este guia detalha os passos necessários para configurar e executar a aplicação Video Display Cycler em um ambiente Linux utilizando Docker e Docker Compose.

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados no seu sistema Linux:

-   **Docker:** [Guia de Instalação do Docker](https://docs.docker.com/engine/install/)
-   **Docker Compose:** [Guia de Instalação do Docker Compose](https://docs.docker.com/compose/install/)

## Configuração Inicial

Siga estes passos apenas na primeira vez que for configurar o projeto.

### 1. Clone o Repositório

Se você ainda não tem os arquivos do projeto, clone o repositório do GitHub:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_SEU_REPOSITORIO>
```

### 2. Crie e Configure o Arquivo de Ambiente (`.env`)

A aplicação usa um arquivo `.env` para gerenciar configurações sensíveis. Crie este arquivo na raiz do projeto.

```bash
touch .env
```

Abra o arquivo `.env` com seu editor de texto preferido (como `nano` ou `vim`) e adicione o seguinte conteúdo.

```ini
# --- Configurações do Django ---
# IMPORTANTE: Gere uma nova chave secreta para produção.
# Você pode usar um gerador online ou o comando:
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY=sua-chave-secreta-aleatoria-e-longa-aqui

# Para desenvolvimento local, pode ser True. Para produção, mude para False.
DEBUG=True

# Permite que qualquer host se conecte. Para produção, seja mais restritivo.
ALLOWED_HOSTS=*

# --- (Opcional) Credenciais para Superusuário Não-Interativo ---
# Se você quiser criar um superusuário automaticamente via script,
# descomente e preencha as linhas abaixo.
# DJANGO_SUPERUSER_USERNAME=admin
# DJANGO_SUPERUSER_PASSWORD=umaSenhaForteEComplexa
# DJANGO_SUPERUSER_EMAIL=admin@example.com
```

**Salve e feche o arquivo.** Este arquivo é ignorado pelo Git (`.gitignore`) e nunca deve ser enviado para o repositório.

### 3. Construa a Imagem Docker

Este comando lê o `Dockerfile` e constrói a imagem da sua aplicação. Isso pode levar alguns minutos na primeira vez.

```bash
docker-compose build
```

### 4. Crie o Banco de Dados e o Superusuário

Com a imagem construída, precisamos inicializar o banco de dados e criar a primeira conta de administrador.

**a. Execute as Migrações:**
Este comando cria o arquivo de banco de dados (`db/db.sqlite3`) com todas as tabelas necessárias.

```bash
docker-compose run --rm web python manage.py migrate
```

**b. Crie a Conta de Superusuário (Modo Interativo):**
Este comando iniciará um processo interativo para você definir o nome de usuário, email e senha do administrador principal.

```bash
docker-compose run --rm web python manage.py createsuperuser
```

Siga as instruções no terminal para completar a criação. Seus dados de login serão salvos de forma segura no banco de dados.

## Executando a Aplicação

Depois de completar a configuração inicial, use os seguintes comandos para gerenciar a aplicação.

### Iniciar o Servidor

Para iniciar a aplicação em segundo plano (modo "detached"):

```bash
docker-compose up -d
```

O servidor web estará rodando e acessível.

-   **Página de Display:** [http://localhost:8000](http://localhost:8000)
-   **Painel de Administração:** [http://localhost:8000/admin](http://localhost:8000/admin)

Para acessar de outros dispositivos na mesma rede, substitua `localhost` pelo endereço IP da máquina que está rodando o Docker (ex: `http://192.168.1.5:8000`).

### Verificar os Logs

Para ver a saída do servidor em tempo real (útil para depuração):

```bash
docker-compose logs -f
```

Pressione `Ctrl + C` para sair da visualização dos logs sem parar o servidor.

### Parar o Servidor

Para parar a aplicação e os contêineres:

```bash
docker-compose down
```

## Manutenção

### Adicionar um Novo Superusuário

Se precisar criar contas de administrador adicionais, basta executar o comando de criação novamente:

```bash
docker-compose run --rm web python manage.py createsuperuser
```

### Reconstruir a Imagem

Se você fizer alterações no código-fonte (como nos arquivos Python, `requirements.txt` ou `Dockerfile`), você precisará reconstruir a imagem antes de iniciar os contêineres novamente.

```bash
# Pare os contêineres, se estiverem rodando
docker-compose down

# Reconstrua a imagem
docker-compose build

# Inicie novamente
docker-compose up -d
```