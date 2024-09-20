
from graphviz import Digraph
from .models import Team

def generate_bracket_visual(modalidade, output_format='svg'):
    try:
        teams = list(Team.objects.filter(modalidade=modalidade).order_by('-points'))
        if not teams:
            return None

        dot = Digraph(comment=f'Chaveamento de {modalidade.nome}', format=output_format)
        dot.attr(rankdir='LR')
        
        team_nodes = []
        for idx, team in enumerate(teams):
            team_node = f"Team{idx}"
            dot.node(team_node, f'{team.name} ({team.points} pts)')
            team_nodes.append(team_node)
        
        while len(team_nodes) > 1:
            next_round = []
            for i in range(0, len(team_nodes), 2):
                if i + 1 < len(team_nodes):
                    match_node = f"Match{len(next_round)}"
                    dot.node(match_node, label='')
                    dot.edge(team_nodes[i], match_node)
                    dot.edge(team_nodes[i + 1], match_node)
                    next_round.append(match_node)
                else:
                    next_round.append(team_nodes[i])
            team_nodes = next_round
        
        output_file = f'bracket_{modalidade.id}.{output_format}'
        dot.render(output_file, view=False, cleanup=False)
        return f"{output_file}.{output_format}"
    
    except Exception as e:
        print(f"Erro ao gerar o bracket visual: {e}")
        return None
    