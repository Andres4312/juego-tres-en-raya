import random
import math
import os

# X is max = 1
# O is min = -1

class TicTacToe:
    def __init__(self):
        self.board = ['-' for _ in range(9)]  # Inicializa el tablero con 9 espacios vacíos
        if random.randint(0, 1) == 1:
            self.humanPlayer = 'X'  # Asigna 'X' al jugador humano
            self.botPlayer = "O"    # Asigna 'O' a la IA
        else:
            self.humanPlayer = "O"  # Asigna 'O' al jugador humano
            self.botPlayer = "X"    # Asigna 'X' a la IA

    def show_board(self):
        print("")  # Imprime una línea en blanco
        for i in range(3):
            # Imprime cada fila del tablero con las casillas separadas por barras verticales
            print("  ", self.board[0 + (i * 3)], " | ", self.board[1 + (i * 3)], " | ", self.board[2 + (i * 3)])
            print("")  # Imprime una línea en blanco

    def is_board_filled(self, state):
        return "-" not in state  # Retorna True si no hay espacios vacíos

    def is_player_win(self, state, player):
        # Combinaciones posibles para ganar: filas, columnas y diagonales
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]  # Diagonales
        ]
        # Verifica si alguna combinación tiene el mismo símbolo del jugador
        return any(state[i] == state[j] == state[k] == player for i, j, k in win_combinations)

    def check_winner(self):
        if self.is_player_win(self.board, self.humanPlayer):
            os.system("cls")  # Limpia la pantalla
            print(f"¡Gano el humano!")  # Imprime mensaje de victoria para el humano
            return True

        if self.is_player_win(self.board, self.botPlayer):
            os.system("cls")  # Limpia la pantalla
            print(f"¡Gano la IA!")  # Imprime mensaje de victoria para la IA
            return True

        if self.is_board_filled(self.board):
            os.system("cls")  # Limpia la pantalla
            print("¡No hay ganador, es un empate!")  # Imprime mensaje de empate
            return True

        return False  # Retorna False si no hay ganador ni empate

    def start(self):
        while True:
            bot = ComputerPlayer(self.botPlayer)  # Inicializa la IA
            human = humanPlayer(self.humanPlayer)  # Inicializa el jugador humano
            game_over = False

            while not game_over:
                os.system("cls")  # Limpia la pantalla
                print(f"Turno del Humano ({self.humanPlayer})")  # Imprime turno del humano
                self.show_board()  # Muestra el tablero

                square = human.human_move(self.board)  # Obtiene el movimiento del humano
                self.board[square] = self.humanPlayer  # Actualiza el tablero con el movimiento del humano
                if self.check_winner():  # Verifica si hay un ganador
                    game_over = True
                    break

                square = bot.machine_move(self.board)  # Obtiene el movimiento de la IA
                self.board[square] = self.botPlayer  # Actualiza el tablero con el movimiento de la IA
                if self.check_winner():  # Verifica si hay un ganador
                    game_over = True
                    break

            self.show_board()  # Muestra el tablero final

            replay = input("¿Quieres jugar de nuevo? (escribe 'si' para volver a jugar / presiona cualquiera tecla para terminar): ").lower()  # Pregunta si se desea jugar de nuevo
            if replay != 'si':
                print("¡Gracias por jugar!")  # Imprime mensaje de agradecimiento
                break
            else:
                self.board = ['-' for _ in range(9)]  #1 Reinicia el tablero para un nuevo juego

class humanPlayer:
    def __init__(self, letter):
        self.letter = letter  # Asigna el símbolo del jugador humano

    def human_move(self, state):
        while True:
            try:
                square = int(input("Ingresa el número de la casilla (1-9) donde quieres jugar: "))  # Solicita el movimiento
                print()
                if 1 <= square <= 9 and state[square - 1] == "-":
                    return square - 1  # Retorna la posición elegida por el humano
                else:
                    print("Esa casilla ya está ocupada o el número es inválido. Elige otra.")  # Mensaje de error si la casilla está ocupada o el número es inválido
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")  # Mensaje de error si la entrada no es un número

class ComputerPlayer(TicTacToe):
    def __init__(self, letter):
        self.botPlayer = letter  # Asigna el símbolo del jugador de la computadora
        self.humanPlayer = "X" if letter == "O" else "O"  # Asigna el símbolo del jugador humano en función del símbolo de la computadora

    def players(self, state):
        x = state.count('X')  # Cuenta cuántas veces aparece 'X'
        o = state.count('O')  # Cuenta cuántas veces aparece 'O'
        return "X" if x == o else "O"  # Retorna el jugador que debe hacer el próximo movimiento

    def actions(self, state):
        return [i for i, x in enumerate(state) if x == "-"]  # Retorna las posiciones vacías en el tablero

    def result(self, state, action):
        newState = state.copy()  # Crea una copia del estado del tablero
        player = self.players(state)  # Obtiene el jugador que debe hacer el movimiento
        newState[action] = player  # Aplica el movimiento en la copia del tablero
        return newState  # Retorna el nuevo estado del tablero

    def terminal(self, state):
        return self.is_player_win(state, "X") or self.is_player_win(state, "O") or self.is_board_filled(state)  # Verifica si el juego ha terminado

    def minimax(self, state, player):
        max_player = self.botPlayer  # El jugador máximo es el de la computadora
        other_player = 'O' if player == 'X' else 'X'  # El otro jugador es el humano

        if self.terminal(state):
            if self.is_player_win(state, max_player):
                return {'position': None, 'score': 1 * (len(self.actions(state)) + 1)}  # Retorna la puntuación para una victoria
            elif self.is_player_win(state, other_player):
                return {'position': None, 'score': -1 * (len(self.actions(state)) + 1)}  # Retorna la puntuación para una derrota
            else:
                return {'position': None, 'score': 0}  # Retorna la puntuación para un empate

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Inicializa el mejor movimiento para el jugador máximo
        else:
            best = {'position': None, 'score': math.inf}  # Inicializa el mejor movimiento para el otro jugador

        for possible_move in self.actions(state):
            newState = self.result(state, possible_move)  # Aplica el movimiento y obtiene el nuevo estado del tablero
            sim_score = self.minimax(newState, other_player)  # Evalúa el movimiento usando minimax
            sim_score['position'] = possible_move  # Actualiza la posición en el resultado simulado

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # Actualiza el mejor movimiento para el jugador máximo
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score  # Actualiza el mejor movimiento para el otro jugador

        return best  # Retorna el mejor movimiento encontrado

    def machine_move(self, state):
        square = self.minimax(state, self.botPlayer)['position']  # Obtiene la mejor posición para la IA usando minimax
        return square  # Retorna la posición seleccionada para la IA
class humanPlayer:
    def __init__(self, letter):
        # Inicializa el jugador humano con su símbolo ('X' o 'O').
        self.letter = letter
    
    def human_move(self, state):
        # Solicita al jugador humano que ingrese su movimiento (posición en el tablero).
        while True:
            try:
                square = int(input("Ingresa el número de la casilla (1-9) donde quieres jugar: "))  # Solicita la posición al jugador
                print()
                # Verifica que la entrada esté en el rango válido (1-9) y que la posición elegida esté vacía.
                if 1 <= square <= 9:
                    if state[square - 1] == "-":
                        return square - 1  # Retorna la posición elegida por el humano
                    else:
                        print("Esa casilla ya está ocupada. Por favor, elige otra.")  # Mensaje si la casilla está ocupada
                else:
                    print("Por favor, ingresa un número entre 1 y 9.")  # Mensaje si el número no está en el rango válido
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")  # Mensaje si la entrada no es un número

class ComputerPlayer(TicTacToe):
    def __init__(self, letter):
        # Inicializa el jugador bot con su símbolo ('X' o 'O') y determina el símbolo del oponente humano.
        self.botPlayer = letter
        self.humanPlayer = "X" if letter == "O" else "O"

    def players(self, state):
        # Determina el jugador actual contando la cantidad de 'X' y 'O' en el tablero.
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if state[i] == "X":
                x += 1  # Cuenta el número de 'X'
            if state[i] == "O":
                o += 1  # Cuenta el número de 'O'
        
        # Determina quién juega según el número de movimientos ya realizados.
        if self.humanPlayer == "X":
            return "X" if x == o else "O"
        if self.humanPlayer == "O":
            return "O" if x == o else "X"
    
    def actions(self, state):
        # Retorna una lista de posiciones vacías disponibles en el tablero.
        return [i for i, x in enumerate(state) if x == "-"]

    def result(self, state, action):
        # Simula el tablero después de realizar un movimiento específico.
        newState = state.copy()  # Crea una copia del estado del tablero
        player = self.players(state)  # Obtiene el jugador que debe hacer el movimiento
        newState[action] = player  # Aplica el movimiento en la copia del tablero
        return newState  # Retorna el nuevo estado del tablero
    
    def terminal(self, state):
        # Determina si el estado actual del tablero es terminal (alguien ha ganado o el tablero está lleno).
        if self.is_player_win(state, "X"):
            return True
        if self.is_player_win(state, "O"):
            return True
        return False

    def minimax(self, state, player):
        max_player = self.humanPlayer  # El jugador humano es el maximizador.
        other_player = 'O' if player == 'X' else 'X'  # El otro jugador es el oponente

        # Verifica si el estado actual es terminal (alguien ganó) o si el tablero está lleno.
        if self.terminal(state):
            return {'position': None, 'score': 1 * (len(self.actions(state)) + 1) if other_player == max_player else -1 * (len(self.actions(state)) + 1)}
        elif self.is_board_filled(state):
            return {'position': None, 'score': 0}  # Retorna 0 si es un empate

        # Si el jugador actual es el maximizador, busca maximizar su puntuación.
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Inicializa con puntuación mínima para maximizar
        else:
            best = {'position': None, 'score': math.inf}  # Inicializa con puntuación máxima para minimizar

        # Explora todos los movimientos posibles.
        for possible_move in self.actions(state):
            newState = self.result(state, possible_move)  # Aplica el movimiento y obtiene el nuevo estado del tablero
            sim_score = self.minimax(newState, other_player)  # Evalúa el movimiento usando minimax

            sim_score['position'] = possible_move  # Representa el movimiento óptimo siguiente

            # Actualiza la mejor puntuación encontrada según el jugador.
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # Actualiza el mejor movimiento para el jugador máximo
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score  # Actualiza el mejor movimiento para el otro jugador

        return best  # Retorna el mejor movimiento encontrado

    def machine_move(self, state):
        # Calcula el mejor movimiento posible usando el algoritmo minimax.
        square = self.minimax(state, self.botPlayer)['position']
        return square  # Retorna la posición seleccionada para la IA

# Inicia el juego
tic_tac_toe = TicTacToe()
tic_tac_toe.start()  # Llama al método start para comenzar el juego
