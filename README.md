📋 Sistema de Finanças Pessoais - Django
Sistema completo para gerenciamento de finanças pessoais desenvolvido em Django com funcionalidades PWA (Progressive Web App).

🚀 Características
✅ Gestão completa de entradas e saídas

✅ Sistema de reservas para objetivos financeiros

✅ PWA - Instalável como app nativo

✅ Interface responsiva para todos os dispositivos

✅ Docker ready

✅ Comandos customizados para testes

📸 Screenshots
(Adicione screenshots do sistema aqui)

🛠️ Tecnologias
Backend: Django 4.2+

Frontend: HTML, CSS, JavaScript

Database: PostgreSQL/SQLite

Container: Docker & Docker Compose

PWA: Service Worker, Web App Manifest

📦 Instalação
Pré-requisitos
Python 3.8+

PostgreSQL (opcional) ou SQLite

Docker (opcional)

Método 1: Docker (Recomendado)
bash
# Clone o repositório
git clone https://github.com/gutosramos/financas_django.git
cd financas_django

# Execute com Docker Compose
docker-compose up -d

# Execute as migrações
docker-compose exec web python manage.py migrate

# Crie um superusuário
docker-compose exec web python manage.py createsuperuser

# Acesse o sistema
# http://localhost:8000
Método 2: Instalação Local
bash
# Clone o repositório
git clone https://github.com/gutosramos/financas_django.git
cd financas_django

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Execute comandos para dados de teste (opcional)
python manage.py criar_dados_teste
python manage.py popular_movimentacoes

# Execute o servidor
python manage.py runserver

# Acesse: http://localhost:8000
⚙️ Configuração
Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto:

env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgres://usuario:senha@localhost:5432/financas
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,.herokuapp.com
Comandos Úteis
bash
# Criar dados de teste
python manage.py criar_dados_teste

# Popular movimentações
python manage.py popular_movimentacoes

# Limpar todos os dados
python manage.py limpar_dados

# Coletar arquivos estáticos
python manage.py collectstatic
📊 Funcionalidades
💰 Gestão Financeira
Entradas: Registro de receitas e rendimentos

Saídas: Controle de despesas e gastos

Reservas: Metas financeiras e objetivos

Dashboard: Visão geral do saldo e transações

📱 PWA Features
✅ Instalação em dispositivos móveis

✅ Funcionamento offline

✅ Interface nativa

✅ Notificações push

🔄 Fluxo de Trabalho
Registre todas as transações

Categorize entradas e saídas

Defina reservas para objetivos

Acompanhe o progresso mensal

🗃️ Estrutura do Projeto
text
financas_django/
├── controle/                 # App principal
│   ├── management/commands/  # Comandos customizados
│   ├── migrations/          # Migrações do banco
│   ├── static/             # Arquivos estáticos (PWA)
│   ├── templates/          # Templates HTML
│   ├── models.py           # Modelos de dados
│   └── views.py            # Lógica da aplicação
├── core/                   # Configurações do projeto
│   ├── settings.py         # Configurações Django
│   └── urls.py            # URLs principais
├── docker-compose.yml      # Orquestração Docker
├── Dockerfile             # Imagem Docker
└── requirements.txt       # Dependências Python
👤 Uso do Sistema
Primeiro Acesso
Acesse http://localhost:8000

Faça login com suas credenciais

Comece registrando suas primeiras transações

Registrando Transações
Nova Entrada: Para receitas e rendimentos

Nova Saída: Para despesas e gastos

Nova Reserva: Para metas financeiras

Dashboard
Visualize saldo atual

Acompanhe últimas transações

Monitore progresso das reservas

🐛 Solução de Problemas
Problemas Comuns
Docker não inicia:

bash
# Reinicie os containers
docker-compose down
docker-compose up -d
Migrações falham:

bash
# Recrie o banco
python manage.py migrate --run-syncdb
Arquivos estáticos não carregam:

bash
python manage.py collectstatic --noinput
📈 Deploy
Heroku
bash
# Configure o buildpack
heroku buildpacks:set heroku/python

# Configure as variáveis de ambiente
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=sua-chave-secreta

# Deploy
git push heroku main
Vercel
Configure como projeto Python

Defina comando de build: pip install -r requirements.txt

Comando de start: python manage.py runserver

🤝 Contribuição
Fork o projeto

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

👨‍💻 Autor
Gutos Ramos

GitHub: @gutosramos

Projeto: financas_django

🙏 Agradecimentos
Equipe Django pelo framework incrível

Comunidade Python Brasil

⭐️ Se este projeto te ajudou, deixe uma estrela no repositório!

<div align="center">
📞 Precisa de ajuda? Abra uma issue no GitHub

</div>