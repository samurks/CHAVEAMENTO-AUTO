from graphviz import Digraph
from .models import Team

def generate_bracket_visual(modalidade, output_format='svg'):
    try:
        teams = list(Team.objects.filter(modalidade=modalidade).order_by('-points'))
        if not teams:
            return None

        dot = Digraph(comment=f'Chaveamento de {modalidade.nome}', format=output_format)
        dot.attr(rankdir='TB', splines='line')

        num_rounds = 1
        while 2 ** num_rounds < len(teams):
            num_rounds += 1

        round_nodes = {i: [] for i in range(num_rounds + 1)}

        for idx, team in enumerate(teams):
            team_node = f"Team{idx}"
            dot.node(team_node, f'{team.name} ({team.points} pts)', shape='rect')
            round_nodes[0].append(team_node)

        current_round = 0
        while current_round < num_rounds:
            next_round_teams = len(round_nodes[current_round]) // 2
            for i in range(next_round_teams):
                match_node = f"Match{current_round}_{i}"
                dot.node(match_node, shape='ellipse', label='')

                team_a = round_nodes[current_round][2 * i]
                team_b = round_nodes[current_round][2 * i + 1]

                dot.edge(team_a, match_node)
                dot.edge(team_b, match_node)
                round_nodes[current_round + 1].append(match_node)

            current_round += 1

        output_file = f'bracket_{modalidade.id}.{output_format}'
        dot.render(output_file, view=False, cleanup=False)
        return f"{output_file}.{output_format}"
    
    except Exception as e:
        print(f"Erro ao gerar o bracket visual: {e}")
        return None
