from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Modalidade
import logging
from django.apps import apps

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def populate_modalidades(sender, **kwargs):
    # Importar modelos aqui, dentro da função, para evitar problemas de carregamento
    from .models import Modalidade

    modalidades = ['Volei', 'Futsal', 'Basket', 'Tenis de Mesa']
    logger.info("Verificando a criação das modalidades...")

    if Modalidade.objects.count() < 3:
        logger.info(f"Modalidades atuais: {Modalidade.objects.all()}")
        for nome in modalidades:
            Modalidade.objects.get_or_create(nome=nome, slug=nome.lower().replace(" ", "_"))
            logger.info(f"Modalidade '{nome}' criada.")
        logger.info("Modalidades criadas com sucesso.")
    else:
        logger.info("Modalidades já estão configuradas no banco de dados.")



@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    # Importando User dentro da função para evitar erros de inicialização
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', '', 'admin123')
        print("Superusuário 'admin' criado com sucesso.")
    else:
        print("Superusuário 'admin' já existe.")
