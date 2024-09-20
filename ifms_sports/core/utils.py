# core/utils.py

from .models import Team

def generate_bracket():
    """
    Gera o chaveamento dos jogos baseado na pontuação dos times.
    """
    teams = list(Team.objects.all().order_by('-points'))  # Ordena os times pela pontuação, do maior para o menor
    bracket = []  # Lista para armazenar os pares de jogos

    while len(teams) >= 2:
        team_a = teams.pop(0)
        team_b = teams.pop(0)
        bracket.append((team_a, team_b))

    if teams:
        # Se sobrar um time, ele avança automaticamente para a próxima fase
        bracket.append((teams[0], None))

    return bracket
