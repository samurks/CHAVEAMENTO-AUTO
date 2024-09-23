from graphviz import Digraph
from .models import Team, Modality
import os

def generate_bracket_visual(modality, output_format='svg'):
    try:
        # Obter times ordenados por data de criação (para garantir ordem de entrada)
        teams = list(Team.objects.filter(modality=modality).order_by('created_at'))
        num_teams = len(teams)
        
        if num_teams == 0:
            print("Nenhum time encontrado para a modality fornecida.")
            return None
        
        # Calcular número de rodadas (potência de 2)
        num_rounds = 1
        while 2 ** num_rounds < num_teams:
            num_rounds += 1
        
        # Gerenciar Byes (caso o número de times não seja potência de 2)
        byes = (2 ** num_rounds) - num_teams
        for _ in range(byes):
            teams.append(None)  # Adiciona espaços vazios para simular "byes"
        
        # Criação do grafo
        dot = Digraph(comment=f'Chaveamento de {modality.nome}', format=output_format)
        dot.attr(rankdir='LR', splines='line', nodesep='1.0', ranksep='1.5')

        round_nodes = {i: [] for i in range(num_rounds + 1)}
        current_round = 0
        
        for idx in range(0, len(teams), 2):
            team_a = teams[idx]
            team_b = teams[idx + 1]
            
            match_node = f"Match{current_round}_{idx//2}"
            label = f'{team_a.name if team_a else "Bye"} vs {team_b.name if team_b else "Bye"}'
            dot.node(match_node, shape='box', label=label)

            if team_a:
                team_node_a = f"Team{idx}"
                dot.node(team_node_a, team_a.name, shape='box')
                dot.edge(team_node_a, match_node)
                round_nodes[current_round].append(team_node_a)

            if team_b:
                team_node_b = f"Team{idx+1}"
                dot.node(team_node_b, team_b.name, shape='box')
                dot.edge(team_node_b, match_node)
                round_nodes[current_round].append(team_node_b)

            round_nodes[current_round + 1].append(match_node)

        for current_round in range(1, num_rounds):
            prev_round_teams = round_nodes[current_round]
            next_round_teams = len(prev_round_teams) // 2

            for i in range(next_round_teams):
                match_node = f"Match{current_round}_{i}"
                dot.node(match_node, shape='box', label='')

                team_a = prev_round_teams[2 * i]
                team_b = prev_round_teams[2 * i + 1]

                dot.edge(team_a, match_node)
                dot.edge(team_b, match_node)
                round_nodes[current_round + 1].append(match_node)

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        output_dir = os.path.join(base_dir, 'ifms_sports', 'static', 'brackets')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f'bracket_{modality.slug}')
        dot.render(output_file, view=False, cleanup=False)
        print(f"Arquivo de chaveamento gerado: {output_file}.{output_format}")
        return f"/static/brackets/bracket_{modality.slug}.{output_format}"
    
    except Exception as e:
        print(f"Erro ao gerar o bracket visual: {e}")
        return None

def populate_modality():
    from .models import Modality

    modality = ['Volei', 'Futsal', 'Basket', 'Tenis de Mesa']

    if Modality.objects.count() < 3:
        for nome in modality:
            Modality.objects.get_or_create(nome=nome, slug=nome.lower().replace(" ", "_"))
