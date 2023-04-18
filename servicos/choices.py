from django.db.models import TextChoices


class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_VELA_MOTOR = 'TVM', 'Troca de vela do motor'
    TROCAR_OLEO = 'TO', 'Troca de Óleo'
    BALANCEAMENTO = 'BL', 'Balanceamento'
