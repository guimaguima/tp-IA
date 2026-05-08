import os
from shutil import move
from typing import List, Tuple, Optional, Dict
import time
import math
import random

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, 1, 2

# -----------------------------------------------------------------------------
# Utilidades de tabuleiro (PRONTAS)
# -----------------------------------------------------------------------------
def copy_board(board: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in board]

def valid_moves(board: List[List[int]]) -> List[int]:
    """Retorna as colunas ainda jogáveis (topo vazio)."""
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def make_move(board: List[List[int]], col: int, player: int) -> Optional[List[List[int]]]:
    """Retorna um novo tabuleiro aplicando a gravidade na coluna col; None se inválido."""
    if col < 0 or col >= COLS or board[0][col] != EMPTY:
        return None
    nb = copy_board(board)
    for r in reversed(range(ROWS)):
        if nb[r][col] == EMPTY:
            nb[r][col] = player
            return nb
    return None

def winner(board: List[List[int]]) -> int:
    """0 se ninguém venceu; 1 ou 2 se há 4 em linha."""
    # Horizontais
    for r in range(ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                return x
    # Verticais
    for c in range(COLS):
        for r in range(ROWS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                return x
    # Diag ↘
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                return x
    # Diag ↗
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                return x
    return 0

def is_full(board: List[List[int]]) -> bool:
    return all(board[0][c] != EMPTY for c in range(COLS))

def terminal(board: List[List[int]]) -> Tuple[bool, int]:
    """(é_terminal, vencedor) com vencedor=0 para empate/indefinido."""
    w = winner(board)
    if w != 0:
        return True, w
    if is_full(board):
        return True, 0
    return False, 0

def other(player: int) -> int:
    return P1 if player == P2 else P2

# -----------------------------------------------------------------------------
# ÚNICO PONTO A SER IMPLEMENTADO PELOS ALUNOS
# -----------------------------------------------------------------------------
def registrar_jogada(modeloA,modeloB,estados_visitados, tempo_jogada, profundidade, arquivo="data/registro_partida_1.csv"):
    precisa_cabecalho = True
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            precisa_cabecalho = False
    except FileNotFoundError:
        pass 

    with open(arquivo, 'a', encoding='utf-8') as f:
        if precisa_cabecalho:
            f.write("ModeloA,ModeloB,Estados Visitados,Tempo por Jogada,Profundidade\n")
        
        estados_str = str(estados_visitados)
        tempo_str = str(tempo_jogada)
        profundidade_str = str(profundidade)

        if ',' in estados_str:
            estados_str = f'"{estados_str}"'
        if ',' in tempo_str:
            tempo_str = f'"{tempo_str}"'
        if ',' in profundidade_str:
            profundidade_str = f'"{profundidade_str}"'

        linha = f"{modeloA},{modeloB},{estados_str},{tempo_str},{profundidade_str}\n"
        
        f.write(linha)

def evaluate(board: List[List[int]], player: int) -> int:
    opponent = other(player)
    score = 0

    is_term, w = terminal(board)
    if is_term:
        if w == player:
            return 1000000 
        elif w == opponent:
            return -1000000
        else:
            return 0

    EVAL_MATRIX = [
        [3, 4, 5,  7,  5, 4, 3],
        [4, 6, 8, 10,  8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10,  8, 6, 4],
        [3, 4, 5,  7,  5, 4, 3]
    ]

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                score += EVAL_MATRIX[r][c]
            elif board[r][c] == opponent:
                score -= EVAL_MATRIX[r][c]

    return score

def min_max(max_turn: bool = False, player: int = 1, turn: int = 1, board: List[List[int]] = None, 
            legal: List[int] = None, time_check=None, max_depth: int = 1, nodes: List[int] = None) -> Tuple[int, int]:

    if nodes is not None:
        nodes[0] += 1

    if time_check():
        return evaluate(board, player), (legal[0] if legal else 0)

    if terminal(board)[0] or (max_depth == 0):
        return evaluate(board, player), 0

    best_move = legal[0] if legal else 0
    best_score = -math.inf if max_turn else math.inf
    
    for col in legal:
        new_board = make_move(board, col, turn)
        
        if new_board is None:
            continue
            
        score, _ = min_max(
            max_turn=not max_turn, 
            player=player, 
            turn=other(turn), 
            board=new_board, 
            legal=valid_moves(new_board),
            time_check=time_check,
            max_depth=(max_depth - 1),
            nodes=nodes
        )
                
        if max_turn:
            if score > best_score:
                best_score = score
                best_move = col
        else:
            if score < best_score:
                best_score = score   
                best_move = col
    
    return best_score, best_move

def alpha_beta(max_turn: bool = False, player: int = 1, turn: int = 1, board: List[List[int]] = None, legal: List[int] = None, 
               time_check=None, max_depth: int = 1, alpha: float = -math.inf, beta: float = math.inf,nodes: List[int] = None) -> Tuple[int, int]:
    
    if nodes is not None:
        nodes[0] += 1
    
    if time_check():
        return evaluate(board, player), (legal[0] if legal else 0)

    if terminal(board)[0] or (max_depth == 0):
        return evaluate(board, player), 0

    best_move = legal[0] if legal else 0
    best_score = -math.inf if max_turn else math.inf
    
    for col in legal:
        new_board = make_move(board, col, turn)
        
        if new_board is None:
            continue
            
        score, _ = alpha_beta(
            max_turn=not max_turn, 
            player=player, 
            turn=other(turn), 
            board=new_board, 
            legal=valid_moves(new_board),
            time_check=time_check,
            max_depth=(max_depth - 1),
            alpha=alpha,
            beta=beta,
            nodes=nodes
        )
            
            
        if max_turn:
            if score > best_score:
                best_score = score
                best_move = col
            
            alpha = max(alpha, best_score)
            
            if best_score >= beta:
                break 
                
        else:
            if score < best_score:
                best_score = score   
                best_move = col
            
            beta = min(beta, best_score)
            
            if best_score <= alpha:
                break
        
    return best_score, best_move
    
def choose_move(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    nodes_visited = [0]
    best_move = 0
    
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return best_move
    
    prefered_order = [3, 2, 4] in legal and [3, 2, 4] or legal
    
    best_move = random.choice(prefered_order)  # Inicializa com uma jogada aleatória válida
    
    #min-max padrão
    # _, move = min_max(
    #     max_turn=True, 
    #     player=turn, 
    #     turn=turn, 
    #     board=board, 
    #     legal=legal, 
    #     time_check=time_exceeded,
    #     max_depth=max_depth,
    #    nodes=nodes_visited   
    # )
    
    # alpha-beta padrão
    # _, move = alpha_beta(
    #     max_turn=True, 
    #     player=turn, 
    #     turn=turn, 
    #     board=board, 
    #     legal=legal, 
    #     time_check=time_exceeded,
    #     max_depth=max_depth,
    #     nodes=nodes_visited
    # )
    
    #interactive deepening
    for depth in range(1, max_depth + 1):
        if time_exceeded():
            print("Time exceeded before starting depth", depth)
            break
        
    #     #com min-max
    #     # _, move = min_max(
    #     #     max_turn=True, 
    #     #     player=turn, 
    #     #     turn=turn, 
    #     #     board=board, 
    #     #     legal=legal, 
    #     #     time_check=time_exceeded,
    #     #     max_depth=depth
    #     #     nodes=nodes_visited
    #     # )
        
    #     # #com alpha-beta
        _, move = alpha_beta(
            max_turn=True, 
            player=turn, 
            turn=turn, 
            board=board, 
            legal=legal, 
            time_check=time_exceeded,
            max_depth=depth,
            nodes=nodes_visited
        )
        
    #     # Só atualiza a melhor jogada se a busca terminou ANTES do tempo acabar
        if not time_exceeded() and move in legal:
            best_move = move
    
    #Usado para os experimentos
    #tempo_total = time.time() - start       
    #registrar_jogada("MinMax","Random", nodes_visited[0], tempo_total, max_depth)
    #registrar_jogada("MinMax","Alpha-Beta", nodes_visited[0], tempo_total, max_depth)
    #registrar_jogada("Alpha-Beta","MinMax", nodes_visited[0], tempo_total, max_depth)
    #registrar_jogada("Alpha-Beta","Iterative Deepening", nodes_visited[0], tempo_total, max_depth)
    #registrar_jogada("Iterative Deepening","Alpha-Beta", nodes_visited[0], tempo_total, max_depth)
    #registrar_jogada("Iterative Deepening","Humano", nodes_visited[0], tempo_total, max_depth)

    return best_move         
        
def choose_move_randomly(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        return move
    
    move = random.choice(legal)
    return move


def choose_move_infinity(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return move
    
    # VERSÃO INICIAL: escolhe aleatoriamente entre as jogadas legais
    i = 0
    while True:
        i += 1

    return move