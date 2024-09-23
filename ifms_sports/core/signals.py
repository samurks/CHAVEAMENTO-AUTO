from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Modality
import logging
from django.apps import apps

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def populate_modality(sender, **kwargs):
    from .models import Modality

    modality = ['Volei', 'Futsal', 'Basket', 'Tenis de Mesa']
    logger.info("Verificando a criação das modality...")

    if Modality.objects.count() < 3:
        logger.info(f"Modalitys atuais: {Modality.objects.all()}")
        for nome in modality:
            Modality.objects.get_or_create(nome=nome, slug=nome.lower().replace(" ", "_"))
            logger.info(f"Modality '{nome}' criada.")
        logger.info("Modalitys criadas com sucesso.")
    else:
        logger.info("Modalitys já estão configuradas no banco de dados.")


@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', '', 'admin123')
        print("Superusuário 'admin' criado com sucesso.")
    else:
        print("Superusuário 'admin' já existe.")
