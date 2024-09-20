# IFMS Sports Management System

## Visão Geral
Este sistema permite o gerenciamento de equipes e jogos para esportes e E-Sports do IFMS.

## Funcionalidades Principais
- Cadastro e gerenciamento de equipes e jogadores.
- Chaveamento automático baseado na pontuação.
- Sistema de login e permissões.
- Envio de notificações por e-mail.

## Instruções para Líderes de Equipe
1. **Cadastro de Equipe**: Após fazer login, o líder pode criar e gerenciar sua equipe.
2. **Gerenciamento de Jogos**: Os líderes podem visualizar e atualizar os detalhes dos jogos.
3. **Atualização de Resultados**: Atualize os resultados dos jogos para refletir a pontuação correta.

## Instruções para Administradores
1. **Acesso ao Sistema**: Use as credenciais `admin` / `admin123` para acessar a área administrativa.
2. **Gerenciamento de Times**: O administrador pode criar, atualizar e excluir qualquer equipe.
3. **Visualização Completa**: O administrador pode visualizar todos os times e jogos.

## Configuração de E-mail
Para enviar notificações por e-mail, configure o backend SMTP no `settings.py`.

## Deployment
O sistema pode ser hospedado usando a Vercel. Certifique-se de que todas as configurações estão corretas antes de fazer o deploy.

## Para rodar o projeto e necessario baixar as dependencias
python3 -m venv env
source env/bin/activate

python manage.py runserver


## Baixar o django no ambiente virtual
pip install django
sudo apt update
sudo apt install python3 python3-pip
sudo apt-get install graphviz
pip install graphviz


## Criar Admin
python manage.py createsuperuser


## Fazer Migracoes para o BD
python manage.py makemigrations
python manage.py migrate
