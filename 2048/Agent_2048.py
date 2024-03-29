from Agent import Agent
from GameBoard import GameBoard
import numpy as np
# MOVES
# LEFT = 0
# UP = 1
# RIGHT = 2
# DOWN = 3

# Posibility of adding a 2 tile 90%
# Posibility of adding a 4 tile 10%


class Agent2048(Agent):
    def __init__(self, max_depth: int = 50):
        super().__init__(max_depth)

    def play(self, board: GameBoard):
        #Debe retornar un movimiento
        action,_ = self.expectimax(board, 4, 1)
        return action

    def heuristic_utility(self, board: GameBoard):
        """
        Una heurisitca que encontramos que servia es:\n
            - Calcular el \"smoothness\" del tablero. Esto es porque cuanto mas \"smooth\" el tablero, mas facil es juntar fichas. Para ello debemos:
                - Aplicar la raiz cuadrada al tablero
                - Sumar la diferencia entre cada casilla y la de abajo
                - Sumar la diferencia entre cada casilla y la de la derecha
                - Elevar este resultado a un smoothness_weight a determinar
                - Multiplicar por -1
            - Calcular el valor del tablero. Esto es porque cuanto mas fichas grandes tengo, mas cerca de ganar estoy. Para ello debemos:
                - Elevar el tablero al cuadrado
                - Sumar todos los valores que se encuentran en el tablero
            - Calcular la cantidad de espacios vacios. Esto es porque cuanto mas espacios vacios tengo, menos chance de tener un mal estado. Para ello debemos:
                - Obtener la cantidad de celdas vacias
                - Multiplicar por un empty_weight (recomendable en el orden de las decenas de miles)
        """
        return self.board_smoothness(board)+ self.board_value(board)+self.board_blank_spaces(board)

    def board_smoothness(self, board, weight: float = 1):
        s_grid = np.sqrt(board.grid)
        
        count = 0
        for x in range(4):
            for y in range(3):
                count += abs(s_grid[x][y] - s_grid[x][y + 1])
        for x in range(3):
            for y in range(4):
                count += abs(s_grid[x][y] - s_grid[x + 1][y])
        return np.power(count , weight) * -1


    def board_value(self, board):
        count = 0
        count = np.sum(np.power(board.grid,2))
        return count
    
    def board_blank_spaces(self, board, weight:float = 5000000):
        return len(board.get_available_cells()) * weight

    #EL AMBIENTE 2048 SE PUEDE MODELAR COMO UN AGENTE QUE TIRA FICHAS DE MANERA RANDOM
    def minimax(self, board: GameBoard, depth, player):
        actions = board.get_available_moves()
        if depth <= 0 or len(actions) == 0:
            return None, self.heuristic_utility(board)

        child_nodes = []
        for action in actions:
            child_node = board.clone()
            child_node.play(action)
            child_nodes.append((action, child_node))

        value = 0
        chosen_action = None
        #mini
        if not player:
            value = float('inf')
            for action_node in child_nodes:
                _, minimax_value = self.minimax(action_node[1], depth - 1, not player)
                if minimax_value <= value:
                    value = minimax_value
        #max
        else:
            value = float('-inf')
            for action_node in child_nodes:
                action, minimax_value = self.minimax(action_node[1], depth - 1, not player)
                if minimax_value >= value:
                    value = minimax_value
                    chosen_action = action_node[0]
        return chosen_action, value

    def expectimax(self, board, depth, player):
        actions = board.get_available_moves()
        if depth <= 0 or len(actions) == 0:
            return None, self.heuristic_utility(board)

        child_nodes = []
        for action in actions:
            child_node = board.clone()
            child_node.play(action)
            child_nodes.append((action, child_node))

        value = 0
        chosen_action = None

        #expecti
        if not player:
            total_child_nodes = len(action_nodes)
            total_value = 0
            for action_node in child_nodes:
                _, expectimax_value = self.exceptimax(action_node[1], depth - 1, not player)
                total_value += expectimax_value
            value = total_value/total_child_nodes
        #max
        else:
            value = float('-inf')
            for action_node in child_nodes:
                action, minimax_value = self.minimax(action_node[1], depth - 1, not player)
                if minimax_value >= value:
                    value = minimax_value
                    chosen_action = action_node[0]

        return chosen_action, value

