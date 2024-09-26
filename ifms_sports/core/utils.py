
from graphviz import Digraph
from .models import Team, Modality
import os

def generate_bracket_visual(modality, output_format='svg'):
    try:
        # Obter times ordenados por data de criação (para garantir ordem de entrada)
        teams = list(Team.objects.filter(modality=modality).order_by('created_at'))
        num_teams = len(teams)
        
        if num_teams == 0:
            print("Nenhum time encontrado para a modalidade fornecida.")
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
        dot.attr(rankdir='LR', splines='line', nodesep='0.3', ranksep='0.5')

        # Determinar o layout desejado (4x4)
        half = len(teams) // 2
        left_teams = teams[:half]
        right_teams = teams[half:]
        
        round_nodes_left = {i: [] for i in range(num_rounds + 1)}
        round_nodes_right = {i: [] for i in range(num_rounds + 1)}
        
        current_round = 0

        # Processar a parte esquerda do bracket
        for idx in range(0, len(left_teams), 2):
            team_a = left_teams[idx]
            team_b = left_teams[idx + 1]

            match_node = f"Left_Match{current_round}_{idx//2}"
            label = f'{team_a.name if team_a else "Bye"} vs {team_b.name if team_b else "Bye"}'
            dot.node(match_node, shape='rect', style='rounded', label=label)

            if team_a:
                team_node_a = f"TeamL{idx}"
                dot.node(team_node_a, team_a.name, shape='rect', style='rounded')
                dot.edge(team_node_a, match_node)
                round_nodes_left[current_round].append(team_node_a)

            if team_b:
                team_node_b = f"TeamL{idx+1}"
                dot.node(team_node_b, team_b.name, shape='rect', style='rounded')
                dot.edge(team_node_b, match_node)
                round_nodes_left[current_round].append(team_node_b)

            round_nodes_left[current_round + 1].append(match_node)

        # Processar a parte direita do bracket
        for idx in range(0, len(right_teams), 2):
            team_a = right_teams[idx]
            team_b = right_teams[idx + 1]

            match_node = f"Right_Match{current_round}_{idx//2}"
            label = f'{team_a.name if team_a else "Bye"} vs {team_b.name if team_b else "Bye"}'
            dot.node(match_node, shape='rect', style='rounded', label=label)

            if team_a:
                team_node_a = f"TeamR{idx}"
                dot.node(team_node_a, team_a.name, shape='rect', style='rounded')
                dot.edge(team_node_a, match_node)
                round_nodes_right[current_round].append(team_node_a)

            if team_b:
                team_node_b = f"TeamR{idx+1}"
                dot.node(team_node_b, team_b.name, shape='rect', style='rounded')
                dot.edge(team_node_b, match_node)
                round_nodes_right[current_round].append(team_node_b)

            round_nodes_right[current_round + 1].append(match_node)

        # Gerar rounds subsequentes e mesclar as linhas
        for current_round in range(1, num_rounds):
            for side, round_nodes in zip(["Left", "Right"], [round_nodes_left, round_nodes_right]):
                prev_round_teams = round_nodes[current_round]
                next_round_teams = len(prev_round_teams) // 2

                for i in range(next_round_teams):
                    merge_node = f"{side}_Merge{current_round}_{i}"
                    dot.node(merge_node, shape='point', width='0')

                    team_a = prev_round_teams[2 * i]
                    team_b = prev_round_teams[2 * i + 1]

                    dot.edge(team_a, merge_node)
                    dot.edge(team_b, merge_node)

                    match_node = f"{side}_Match{current_round}_{i}"
                    dot.node(match_node, shape='rect', style='rounded', label='')
                    dot.edge(merge_node, match_node)
                    round_nodes[current_round + 1].append(match_node)

        # Mesclar lado esquerdo e direito no centro
        center_merge_node = "Center_Merge"
        dot.node(center_merge_node, shape='point', width='0')

        final_left = round_nodes_left[num_rounds][0] if round_nodes_left[num_rounds] else None
        final_right = round_nodes_right[num_rounds][0] if round_nodes_right[num_rounds] else None

        # Verificar se ambos os lados estão completos
        if final_left and final_right:
            dot.edge(final_left, center_merge_node)
            dot.edge(final_right, center_merge_node)
        else:
            print("Erro: As finais do chaveamento não estão completas.")
            return None

        final_match_node = "Final_Match"
        dot.node(final_match_node, shape='rect', style='rounded', label='')
        dot.edge(center_merge_node, final_match_node)

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