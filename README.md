# 🚀 Video Display Cycler

Video Display Cycler é uma aplicação de sinalização digital (digital signage) construída com Django. Ela permite gerenciar e exibir um ciclo contínuo de vídeos e imagens em tela cheia através de uma interface web simples.

A aplicação foi projetada para ser flexível, podendo ser executada como um aplicativo de desktop autônomo no Windows ou como um serviço conteinerizado no Linux.

## ✨ Funcionalidades

*   **Conteúdo Misto:** Exibe vídeos (.mp4) e imagens estáticas (.png, .jpg) em um ciclo contínuo.
*   **Duração Configurável:** Defina por quantos segundos cada imagem estática deve ser exibida.
*   **Gerenciamento Web:** Adicione, remova e reordene o conteúdo facilmente através do painel de administração do Django.
*   **Atualização em Tempo Real:** Os displays atualizam automaticamente a lista de reprodução periodicamente, sem a necessidade de reiniciar.
*   **Executável para Windows:** Empacotado em um único arquivo `.exe` com um painel de controle gráfico (GUI) para facilitar o uso por não-desenvolvedores.
*   **Pronto para Docker:** Inclui um `Dockerfile` e `docker-compose.yml` para implantação rápida e consistente em ambientes Linux.
*   **Acesso via Rede Local:** O servidor pode ser configurado para ser acessível a partir de outros dispositivos na mesma rede.
*   **Builds Automatizados:** O workflow de GitHub Actions compila e cria uma nova Release no GitHub automaticamente a cada merge de Pull Request.

---

## 📖 Tabela de Conteúdos

*   [Guia Rápido para Usuários Windows](#-guia-rápido-para-usuários-windows-executando-o-exe)
*   [Guia Rápido para Desenvolvedores (Docker em Linux)](#-guia-rápido-para-desenvolvedores-docker-em-linux)
*   [Como Usar a Aplicação](#-como-usar-a-aplicação)
*   [Desenvolvimento e Builds Automatizados](#-desenvolvimento-e-builds-automatizados)
*   [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🖥️ Guia Rápido para Usuários Windows (Executando o .exe)

Esta seção é para usuários que desejam apenas executar a aplicação no Windows sem se preocupar com código ou configuração.

### 1. Baixe a Última Versão

Vá para a seção de **[Releases](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/releases)** do repositório no GitHub.

Procure pela release mais recente e baixe o arquivo `.zip` (ex: `VideoDisplay-PR-XX.zip`).

### 2. Descompacte os Arquivos

Extraia o conteúdo do arquivo `.zip` para uma pasta de sua escolha. Você terá dois arquivos principais:

*   `VideoDisplay.exe`
*   `db.sqlite3`

**IMPORTANTE:** Mantenha sempre o arquivo `db.sqlite3` na mesma pasta que o `VideoDisplay.exe`. Ele armazena todos os seus dados.

### 3. Execute a Aplicação

Dê um duplo clique em `VideoDisplay.exe`. Um painel de controle irá aparecer.

### 4. Use o Painel de Controle

*   **Host e Porta:** Deixe os valores padrão (`0.0.0.0` e `8000`) para acesso na rede local.
*   **Iniciar Servidor:** Clique para iniciar o serviço de display.
*   **Abrir Display:** Abre a tela de exibição em tela cheia no seu navegador.
*   **Acessar Admin:** Abre o painel de administração para gerenciar o conteúdo.
*   **Criar Superusuário:** Se você precisar criar uma conta de administrador (ou resetar a sua), clique aqui. Uma nova janela de terminal aparecerá para guiá-lo.
*   **Parar Servidor:** Para o serviço Django, permitindo que você altere a configuração e inicie novamente.
*   Feche a janela para encerrar a aplicação completamente.

**Nota sobre o Primeiro Acesso:** O banco de dados já vem com um superusuário padrão criado durante o processo de build. **É altamente recomendável que você acesse o painel de administração e altere a senha padrão no primeiro uso.**

---

## 🐧 Guia Rápido para Desenvolvedores (Docker em Linux)

Esta seção é para desenvolvedores que desejam executar a aplicação a partir do código-fonte usando Docker.

### Pré-requisitos

*   Git
*   Docker
*   Docker Compose

### 1. Clone o Repositório e Navegue até a Pasta

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Crie e Configure o Arquivo `.env`

A aplicação usa um arquivo `.env` para configurações. Crie-o a partir do template:

```bash
touch .env
```

Abra o arquivo (`nano .env`) e adicione o seguinte conteúdo, substituindo os valores conforme necessário:

```ini
# Gere uma nova chave em https://djecrety.ir/
SECRET_KEY=sua-chave-secreta-aleatoria-aqui
DEBUG=True
ALLOWED_HOSTS=*
```

### 3. Construa a Imagem Docker

```bash
docker-compose build
```

### 4. Inicialize o Banco de Dados (Apenas na Primeira Vez)

Você **precisa** executar estes comandos na primeira vez para criar as tabelas do banco de dados e sua conta de administrador.

**a. Execute as Migrações:**
```bash
docker-compose run --rm web python manage.py migrate```
```

**b. Crie sua Conta de Superusuário:**
```bash
docker-compose run --rm web python manage.py createsuperuser
```
Siga as instruções interativas no terminal.

### 5. Execute a Aplicação

Use os seguintes comandos para gerenciar o servidor:

*   **Iniciar o servidor em segundo plano:**
    ```bash
    docker-compose up -d
    ```
*   **Ver os logs em tempo real:**
    ```bash
    docker-compose logs -f
    ```
*   **Parar o servidor:**
    ```bash
    docker-compose down
    ```

---

## 🚀 Como Usar a Aplicação

Após iniciar o servidor (seja pelo `.exe` ou pelo Docker), o uso é o mesmo.

1.  **Acesse o Painel de Administração:** Abra seu navegador e vá para `http://127.0.0.1:8000/admin`. Se estiver acessando de outra máquina na rede, use o IP do computador hospedeiro (ex: `http://192.168.1.5:8000/admin`).

2.  **Faça o Login:** Use as credenciais de superusuário que você criou.

3.  **Adicione Conteúdo:**
    *   No painel, encontre a seção "VIDEOCYCLER" e clique em "Adicionar" ao lado de "Display items".
    *   Preencha os campos:
        *   **Title:** Um nome para sua referência (ex: "Vídeo de Abertura").
        *   **Media type:** Escolha "Vídeo" ou "Imagem".
        *   **File:** Clique para fazer o upload do seu arquivo `.mp4`, `.png`, `.jpg`, etc.
        *   **Duration in seconds:** **Apenas para imagens.** Defina por quantos segundos a imagem deve ficar na tela.
        *   **Order:** Defina a ordem de exibição (0, 1, 2, ...). Itens com números menores aparecem primeiro.
    *   Clique em "Salvar".

4.  **Visualize o Display:**
    *   Abra um navegador (idealmente em uma segunda tela) e vá para `http://127.0.0.1:8000/`. O ciclo de vídeos e imagens começará automaticamente.

---

## 🛠️ Desenvolvimento e Builds Automatizados

Este projeto utiliza **GitHub Actions** para automatizar o processo de build e release.

*   **Gatilho:** Uma nova release é criada sempre que um **Pull Request é mergeado** na branch `main`.
*   **Processo:** A action executa todos os passos necessários (instalação de dependências, migrações, `collectstatic`, criação de superusuário padrão) em um ambiente Windows limpo.
*   **Resultado:** Um arquivo `VideoDisplay-PR-XX.zip` é gerado e anexado a uma nova Release no GitHub. O título da Release é preenchido automaticamente com o título do Pull Request.

---

## 📂 Estrutura do Projeto

```
.
├── .github/workflows/build.yml   # Workflow do GitHub Actions para build e release
├── core/                           # Projeto principal do Django
│   ├── settings.py                 # Configurações do projeto (lógica multi-ambiente)
│   └── urls.py                     # URLs do projeto
├── videoCycler/                    # App principal do Django
│   ├── models.py                   # Modelos do banco de dados (DisplayItem)
│   ├── views.py                    # Views do Django
│   └── templates/                  # Template HTML do display
├── admin_setup.py                  # Lógica para criar o superusuário interativamente
├── run_app.py                      # Ponto de entrada para o executável do Windows (GUI com Tkinter)
├── Dockerfile                      # Receita para construir a imagem Docker
├── docker-compose.yml              # Orquestração do contêiner Docker
├── VideoDisplay.spec               # "Receita" do PyInstaller para o .exe
└── README.md                       # Este arquivo
```