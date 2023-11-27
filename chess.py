import pygame
import sys
import copy
from enum import Enum

# Define constants
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 6, 6
SQUARE_SIZE = WIDTH // COLS
DEPTH = 3


class GameMode(Enum):
    USER_VS_USER = 1
    USER_VS_BOT = 2
    BOT_VS_BOT = 3


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)


def display_game_mode_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Mode Selection")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    while True:
        screen.fill((255, 255, 255))

        for i, option in enumerate(["User vs User", "User vs Bot", "Bot vs Bot"]):
            text = font.render(option, True, (0, 0, 0))
            screen.blit(text, (50, 10 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 < x < 250:
                    selected_mode = GameMode((y - 10) // 40 + 1)
                    return selected_mode

        clock.tick(60)


# Initialize pygame
pygame.init()


def show_popup(message, text_color):
    popup_font = pygame.font.Font(None, 36)
    popup_text = popup_font.render(message, True, text_color)
    popup_rect = popup_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    pygame.draw.rect(
        screen,
        WHITE,
        (
            popup_rect.x - 10,
            popup_rect.y - 10,
            popup_rect.width + 20,
            popup_rect.height + 20,
        ),
    )
    screen.blit(popup_text, popup_rect.topleft)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display the pop-up for 2 seconds
    # Reset the caption


# Create the chess board
chess_board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Set up initial chess pieces
chess_board[0] = ["br", "bn", "bq", "bk", "bn", "br"]
chess_board[1] = ["bp", "bp", "bp", "bp", "bp", "bp"]
chess_board[4] = ["wP", "wP", "wP", "wP", "wP", "wP"]
chess_board[5] = ["wR", "wN", "wQ", "wK", "wN", "wR"]

# Initialize pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess 6x6")

original_white_queen_image = pygame.image.load(r"image\wQ.png")
original_black_queen_image = pygame.image.load(r"image\bQ.png")

original_white_king_image = pygame.image.load(r"image\wK.png")
original_black_king_image = pygame.image.load(r"image\bK.png")

original_white_queen_image = pygame.image.load(r"image\wQ.png")
original_black_queen_image = pygame.image.load(r"image\bQ.png")

original_white_rook_image = pygame.image.load(r"image\wR.png")
original_black_rook_image = pygame.image.load(r"image\bR.png")

original_white_knight_image = pygame.image.load(r"image\wN.png")
original_black_knight_image = pygame.image.load(r"image\bN.png")

original_white_pawn_image = pygame.image.load(r"image\wp.png")
original_black_pawn_image = pygame.image.load(r"image\bp.png")  # Update the path here

# Resize images to fit into squares
piece_image_size = (SQUARE_SIZE, SQUARE_SIZE)
pawn_image_size = (SQUARE_SIZE, SQUARE_SIZE)

white_queen_image = pygame.transform.scale(original_white_queen_image, piece_image_size)
black_queen_image = pygame.transform.scale(original_black_queen_image, piece_image_size)

white_king_image = pygame.transform.scale(original_white_king_image, piece_image_size)
black_king_image = pygame.transform.scale(original_black_king_image, piece_image_size)

white_rook_image = pygame.transform.scale(original_white_rook_image, piece_image_size)
black_rook_image = pygame.transform.scale(original_black_rook_image, piece_image_size)

white_queen_image = pygame.transform.scale(original_white_queen_image, piece_image_size)
black_queen_image = pygame.transform.scale(original_black_queen_image, piece_image_size)

white_knight_image = pygame.transform.scale(
    original_white_knight_image, piece_image_size
)
black_knight_image = pygame.transform.scale(
    original_black_knight_image, piece_image_size
)

white_pawn_image = pygame.transform.scale(original_white_pawn_image, pawn_image_size)
black_pawn_image = pygame.transform.scale(original_black_pawn_image, pawn_image_size)


# ... (rest of your code)
def evaluate_board(board):
    # This is a simple evaluation function that counts the material advantage for white
    white_score = 0
    black_score = 0

    for row in board:
        for piece in row:
            if piece != " ":
                if piece[0] == "w":
                    white_score += 1
                else:
                    black_score += 1

    return white_score - black_score


def minimax(board, depth, maximizing_player):
    if depth == 0:
        return evaluate_board(board)

    valid_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " " and piece[0] == "b":
                moves = get_valid_moves(board, row, col)
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_board[move[0]][move[1]] = new_board[row][col]
                    new_board[row][col] = " "
                    score = minimax(new_board, depth - 1, False)
                    valid_moves.append((move, score))

    if maximizing_player:
        best_move = max(valid_moves, key=lambda x: x[1])
        return best_move[1]
    else:
        best_move = min(valid_moves, key=lambda x: x[1])
        return best_move[1]


def ai_make_move(board):
    valid_moves = []

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " " and piece[0] == "b":
                moves = get_valid_moves(board, row, col)
                for move in moves:
                    new_board = copy.deepcopy(board)
                    new_board[move[0]][move[1]] = new_board[row][col]
                    new_board[row][col] = " "
                    # Evaluate the move by considering the captured piece's value
                    score = evaluate_board(new_board) + piece_value(
                        board[move[0]][move[1]]
                    )
                    valid_moves.append(((row, col), move, score))

    best_move = max(valid_moves, key=lambda x: x[2])
    return best_move[0], best_move[1]


def piece_value(piece):
    # Check if the piece is not an empty string
    if piece != " ":
        # Assign values to pieces for evaluation
        if piece[1].lower() == "p":
            return 1
        elif piece[1].lower() == "r":
            return 5
        elif piece[1].lower() == "n":
            return 3
        elif piece[1].lower() == "b":
            return 3
        elif piece[1].lower() == "q":
            return 9
        elif piece[1].lower() == "k":
            return 100  # King's value is high to prioritize keeping the king safe

    return 0  # Default value for empty squares


def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )
            piece = chess_board[row][col]
            if piece != " ":
                if piece[1].lower() == "p":  # Check if it's a pawn
                    image = white_pawn_image if piece[0] == "w" else black_pawn_image
                elif piece[1].lower() == "q":  # Queen
                    image = white_queen_image if piece[0] == "w" else black_queen_image
                elif piece[1].lower() == "k":  # King
                    image = white_king_image if piece[0] == "w" else black_king_image
                elif piece[1].lower() == "r":  # Rook
                    image = white_rook_image if piece[0] == "w" else black_rook_image
                elif piece[1].lower() == "n":  # Knight
                    image = (
                        white_knight_image if piece[0] == "w" else black_knight_image
                    )
                else:
                    font = pygame.font.Font(None, 36)
                    text = font.render(piece, True, BLACK)
                    screen.blit(
                        text,
                        (
                            col * SQUARE_SIZE + SQUARE_SIZE // 3,
                            row * SQUARE_SIZE + SQUARE_SIZE // 4,
                        ),
                    )
                    continue  # Skip drawing the piece as an image if it's not a pawn, queen, king, rook, or knight

                screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))


# ... (rest of your code)


def get_pawn_moves(board, row, col):
    moves = []
    direction = (
        1 if board[row][col][0] == "b" else -1
    )  # Direction depends on the color of the pawn

    # Check one square ahead
    new_row = row + direction
    if 0 <= new_row < ROWS and board[new_row][col] == " ":
        moves.append((new_row, col))

        # If pawn is in its starting position, it can move two squares ahead
        # if ((row == 1 and direction == 1) or (row == 4 and direction == -1)) and board[
        #     new_row + direction
        # ][col] == " ":
        #     moves.append((new_row + direction, col))

    # Check diagonal captures
    for col_offset in [-1, 1]:
        new_col = col + col_offset
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
            and board[new_row][new_col] != " "
            and board[new_row][new_col][0] != board[row][col][0]
        ):
            moves.append((new_row, new_col))

    return moves


def promote_pawn(board, row, col):
    # Display a promotion menu
    promotion_options = ["Q", "R", "N"]
    selected_piece = promotion_menu()

    # Promote the pawn to the selected piece
    color = board[row][col][0]
    board[row][col] = color + selected_piece

    # Update the display after promotion
    draw_board()
    pygame.display.flip()
    pygame.time.delay(1000)


def promotion_menu():
    promotion_options = ["Queen", "Rook", "N"]
    images = {
        "Queen": white_queen_image,
        "Rook": white_rook_image,
        "N": white_knight_image,
        # "B": white_bishop_image,  # Assuming you have a bishop image
    }

    # Pygame setup for the promotion menu
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Promotion Menu")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Button dimensions
    button_width = 200
    button_height = 80
    button_margin = 20

    buttons = []
    for i, option in enumerate(promotion_options):
        button_rect = pygame.Rect(
            120,
            20 + i * (button_height + button_margin),
            button_width,
            button_height,
        )
        buttons.append((button_rect, option))

    # Display promotion options
    while True:
        screen.fill((255, 255, 255))

        for button_rect, option in buttons:
            pygame.draw.rect(screen, (200, 200, 200), button_rect)
            text = font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

            image = images[option]
            image_rect = image.get_rect(topleft=(button_rect.right + 20, button_rect.y))
            screen.blit(image, image_rect)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button_rect, selected_piece in buttons:
                    if button_rect.collidepoint(x, y):
                        return selected_piece

        clock.tick(60)


def get_knight_moves(board, row, col):
    moves = []

    offsets = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

    for offset in offsets:
        new_row, new_col = row + offset[0], col + offset[1]
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
            and board[new_row][new_col][0] != board[row][col][0]
        ):
            moves.append((new_row, new_col))

    return moves


def get_rook_moves(board, row, col):
    moves = []

    # Check vertically
    for new_row in range(row - 1, -1, -1):  # Check upward
        if board[new_row][col] == " ":
            moves.append((new_row, col))
        else:
            if (
                board[new_row][col][0] != board[row][col][0]
            ):  # Capture if opposite color
                moves.append((new_row, col))
            break

    for new_row in range(row + 1, ROWS):  # Check downward
        if board[new_row][col] == " ":
            moves.append((new_row, col))
        else:
            if (
                board[new_row][col][0] != board[row][col][0]
            ):  # Capture if opposite color
                moves.append((new_row, col))
            break

    # Check horizontally
    for new_col in range(col - 1, -1, -1):  # Check leftward
        if board[row][new_col] == " ":
            moves.append((row, new_col))
        else:
            if (
                board[row][new_col][0] != board[row][col][0]
            ):  # Capture if opposite color
                moves.append((row, new_col))
            break

    for new_col in range(col + 1, COLS):  # Check rightward
        if board[row][new_col] == " ":
            moves.append((row, new_col))
        else:
            if (
                board[row][new_col][0] != board[row][col][0]
            ):  # Capture if opposite color
                moves.append((row, new_col))
            break

    return moves


def get_bishop_moves(board, row, col):
    moves = []

    # Check diagonally
    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_row, new_col = row + offset[0], col + offset[1]
        while 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if board[new_row][new_col] == " ":
                moves.append((new_row, new_col))
            elif (
                board[new_row][new_col][0] != board[row][col][0]
            ):  # Capture if opposite color
                moves.append((new_row, new_col))
                break
            else:
                break
            new_row += offset[0]
            new_col += offset[1]

    return moves


def get_queen_moves(board, row, col):
    moves = []

    moves.extend(get_rook_moves(board, row, col))
    moves.extend(get_bishop_moves(board, row, col))

    return moves


def get_king_moves(board, row, col):
    moves = []

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for offset in offsets:
        new_row, new_col = row + offset[0], col + offset[1]
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
            and board[new_row][new_col][0] != board[row][col][0]
        ):
            moves.append((new_row, new_col))

    return moves


def get_valid_moves(board, row, col):
    piece = board[row][col]

    if piece[1].lower() == "p":
        moves = get_pawn_moves(board, row, col)
        if row == 0 or row == ROWS - 1:
            # Check if pawn reached the opposite end
            moves += get_moves_after_promotion(board, row, col, piece)
        return moves
    elif piece[1].lower() == "r":
        return get_rook_moves(board, row, col)
    elif piece[1].lower() == "n":
        return get_knight_moves(board, row, col)
    elif piece[1].lower() == "b":
        return get_bishop_moves(board, row, col)
    elif piece[1].lower() == "q":
        return get_queen_moves(board, row, col)
    elif piece[1].lower() == "k":
        return get_king_moves(board, row, col)

    # Add more logic for other pieces here if needed

    return []


def get_moves_after_promotion(board, row, col, piece_after_promotion):
    # Use the appropriate function based on the promoted piece type
    piece_type = piece_after_promotion[1].lower()
    if piece_type == "q":
        return get_queen_moves(board, row, col)
    elif piece_type == "r":
        return get_rook_moves(board, row, col)
    elif piece_type == "n":
        return get_knight_moves(board, row, col)
    elif piece_type == "b":
        return get_bishop_moves(board, row, col)
    elif piece_type == "k":
        return get_king_moves(board, row, col)
    else:
        return []


def is_check(board, current_player):
    king_position = None  # Initialize king_position here

    # Find the king's position for the current player
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " " and piece[0] == current_player and piece[1].lower() == "k":
                king_position = (row, col)
                break

    # Check if any opponent's piece can capture the king
    opponent_player = "w" if current_player == "b" else "b"
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != " " and board[row][col][0] == opponent_player:
                moves = get_valid_moves(board, row, col)
                if king_position in moves:
                    return True

    return False


def highlight_square(row, col, color):
    pygame.draw.rect(
        screen,
        color,
        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        5,  # Thickness of the highlight border
    )


def is_checkmate(board, current_player):
    # Check if the current player is in check
    if not is_check(board, current_player):
        return False  # Not in check, so not in checkmate

    # Check if any move by the current player can get out of check
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " " and piece[0] == current_player:
                moves = get_valid_moves(board, row, col)
                for move in moves:
                    # Simulate the move and check if it gets out of check
                    new_board = copy.deepcopy(board)
                    new_board[move[0]][move[1]] = new_board[row][col]
                    new_board[row][col] = " "
                    if not is_check(new_board, current_player):
                        return False  # At least one move gets out of check

    # Check if any opponent's piece can be captured to get out of check
    opponent_player = "w" if current_player == "b" else "b"
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != " " and board[row][col][0] == opponent_player:
                moves = get_valid_moves(board, row, col)
                for move in moves:
                    # Simulate the move and check if it gets out of check
                    new_board = copy.deepcopy(board)
                    new_board[move[0]][move[1]] = new_board[row][col]
                    new_board[row][col] = " "
                    if not is_check(new_board, current_player):
                        return False  # At least one move captures an opponent's piece and gets out of check

    return True  # No moves get out of check, so it's checkmate


def draw_check_status(screen, font, current_player, is_in_check):
    check_message = f"{current_player.upper()} is in CHECK!" if is_in_check else ""
    text = font.render(check_message, True, (255, 0, 0))  # Red color for check message
    screen.blit(text, (10, 10))


def main():
    selected_mode = display_game_mode_menu()
    current_player = "w"  # Initialize outside the loop

    if selected_mode == GameMode.USER_VS_USER:
        # No additional setup needed for user vs user
        pass
    elif selected_mode == GameMode.USER_VS_BOT:
        # If user chooses user vs bot, the second player will be the bot
        pass
    elif selected_mode == GameMode.BOT_VS_BOT:
        # If user chooses bot vs bot, both players will be bots
        pass

    selected_piece = None
    row, col = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = event.pos[1] // SQUARE_SIZE

                piece = chess_board[row][col]

                if selected_piece is None:
                    if piece != " " and piece[0] == current_player[0]:
                        selected_piece = (row, col)
                else:
                    if (row, col) in get_valid_moves(
                        chess_board, selected_piece[0], selected_piece[1]
                    ):
                        # Perform the move
                        chess_board[row][col] = chess_board[selected_piece[0]][
                            selected_piece[1]
                        ]
                        chess_board[selected_piece[0]][selected_piece[1]] = " "
                        selected_piece = None
                        current_player = (
                            "b" if current_player == "w" else "w"
                        )  # Switch turns
                        print(f"It is {current_player.upper()}'s turn.")
                        if selected_mode != GameMode.USER_VS_USER:
                            # AI's turn for both players in bot vs bot
                            ai_from_square, ai_to_square = ai_make_move(chess_board)
                            chess_board[ai_to_square[0]][ai_to_square[1]] = chess_board[
                                ai_from_square[0]
                            ][ai_from_square[1]]
                            chess_board[ai_from_square[0]][ai_from_square[1]] = " "
                            current_player = (
                                "w" if current_player == "b" else "b"
                            )  # Switch turns for the bots

                    elif piece != " " and piece[0] == current_player[0]:
                        # Change the selected piece
                        selected_piece = (row, col)
                    else:
                        # Cancel the selection if clicking on an empty space or opponent's piece
                        selected_piece = None

        if current_player == "w" and selected_mode == GameMode.USER_VS_BOT:
            if row == 0 and chess_board[row][col][1].lower() == "p":
                # Pawn reached the opposite end for white
                promote_pawn(chess_board, row, col)

        if current_player == "b" and selected_mode != GameMode.USER_VS_USER:
            # AI's turn for both players in bot vs bot
            ai_from_square, ai_to_square = ai_make_move(chess_board)
            chess_board[ai_to_square[0]][ai_to_square[1]] = chess_board[
                ai_from_square[0]
            ][ai_from_square[1]]
            chess_board[ai_from_square[0]][ai_from_square[1]] = " "
            current_player = (
                "w" if current_player == "b" else "b"
            )  # Switch turns for the bots

        if is_check(chess_board, current_player[0]):
            print(f"{current_player.upper()} is in CHECK!")

        if is_checkmate(chess_board, current_player[0]):
            print(f"{current_player.upper()} is in CHECKMATE! Game Over.")
            show_popup(f"{current_player.upper()} is in CHECKMATE! Game Over.", BLACK)
            pygame.quit()
            sys.exit()

        draw_board()

        if selected_piece is not None:
            highlight_square(
                selected_piece[0], selected_piece[1], (255, 0, 0)
            )  # Red for selected piece
            moves = get_valid_moves(chess_board, selected_piece[0], selected_piece[1])
            for move in moves:
                highlight_square(
                    move[0], move[1], (0, 255, 0)
                )  # Green for possible moves

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
