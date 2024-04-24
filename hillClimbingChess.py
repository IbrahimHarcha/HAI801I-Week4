import chess

# on définit les valeurs des pièces et les pénalités/bonus
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3.25,
    chess.BISHOP: 3.25,
    chess.ROOK: 5,
    chess.QUEEN: 9.75,
    chess.KING: 0,
}

ISOLATED_PAWN_PENALTY = {
    0: -0.12,  # 'a' file
    1: -0.14,  # 'b' file
    2: -0.16,  # 'c' file
    3: -0.20,  # 'd' file
    4: -0.20,  # 'e' file
    5: -0.16,  # 'f' file
    6: -0.14,  # 'g' file
    7: -0.12,  # 'h' file
}

DOUBLED_PAWN_PENALTY = -0.12
BACKWARD_PAWN_PENALTY = -0.06
BACKWARD_PAWN_ATTACK_BONUS = 0.04
PAWN_ADVANCE_BONUS = 0.04

# fonction d'évaluation qui prend en compte les pénalités et bonus
def evaluate_board(board):
    total_value = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES.get(piece.piece_type, 0)
            if piece.color == chess.BLACK:
                value = -value
            total_value += value

            # pénalités pour les pions isolés et doublés...
            if piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                if all(board.piece_at(chess.square(file, rank)) is None for rank in range(8) if rank != chess.square_rank(square)):
                    total_value += ISOLATED_PAWN_PENALTY[file]

                same_file_pawns = sum(board.piece_at(chess.square(file, r)) is not None for r in range(8))
                if same_file_pawns > 1:
                    total_value += DOUBLED_PAWN_PENALTY

                if file in [3, 4]:  # 'd' et 'e' files
                    total_value += PAWN_ADVANCE_BONUS * chess.square_rank(square)

    return total_value

# Fonction de hill climbing pour trouver le meilleur coup
def hill_climb(board):
    legal_moves = list(board.legal_moves)

    best_move = None
    best_score = -float("inf")

    for move in legal_moves:
        board.push(move)

        # si le mouvement met l'adversaire en échec et mat, c'est le meilleur mouvement
        if board.is_checkmate():
            best_move = move
            best_score = float("inf")  # Échec et mat
            board.pop()
            break

        # on évite les mouvements qui mettent en échec
        if board.is_check():
            board.pop()
            continue

        score = evaluate_board(board)

        if score > best_score:
            best_move = move
            best_score = score

        board.pop()

    return best_move, best_score

# on initialise l'échiquier avec la position donnée
fen = "8/2BPR3/B3P3/3P1P2/p6R/5p2/P1p2b1K/3k2N1 w - - 0 1"
board = chess.Board(fen)

print("Position de base : ")
print(board)

# # trouve le meilleur coup
# best_move, best_score = hill_climb(board)

# print("Meilleur coup :", best_move)
# print("Score du meilleur coup :", best_score)

# le nombre de coup à exécuter
number_of_moves = 3

for i in range(number_of_moves):
    if i == 0:
        print("Premier coup :")
    else:
        print(f"{i + 1}ème coup :")
    best_move, best_score = hill_climb(board)
    if best_move is None:
        print("Aucun mouvement valide trouvé (c'est peut être la fin de la partie)")
        break
    print("Meilleur coup :", best_move)
    print("Score du meilleur coup :", best_score)
    board.push(best_move)
    print(board)